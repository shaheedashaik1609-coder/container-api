import oracledb
from fastapi import APIRouter, Depends, HTTPException

from app.db import get_conn
from app.schemas import ContainerCreate, ContainerOut
from app.security import verify_key

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    dependencies=[Depends(verify_key)],
)

@router.get("/{container_id}", response_model=ContainerOut)
def get_container(container_id: str, conn = Depends(get_conn)):
    with conn.cursor() as cur:
       cur.execute("SELECT container_id, size_ft, weight_kg, destination, status FROM containers WHERE container_id = :id""",id=container_id)
       row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Container not found")
    return ContainerOut(container_id=row[0], size=row[1], weight_kg=row[2], destination=row[3], status=row[4])  

@router.get("", response_model=list[ContainerOut])
def list_containers(status: str | None = None, limit: int = 50, offset: int = 0, conn = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM containers")
        rows = cur.fetchall()
        return [ContainerOut(**row) for row in rows]

@router.post("", response_model=ContainerOut)
def create_container(container: ContainerCreate, conn: oracledb.Connection = Depends(get_conn)):
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO containers (id, name, size) VALUES (:id, :name, :size)", {
            "id": container.id,
            "name": container.name,
            "size": container.size
            })
        conn.commit()
    except oracledb.IntegrityError:
            raise HTTPException(status_code=409, detail="Container already exists")
    return ContainerOut(**container.model_dump(), status="IN_YARD")

@router.patch("/{container_id}/status")
def update_status(container_id: str, status: str, conn: oracledb.Connection = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("UPDATE containers SET status = :status WHERE id = :id", {"status": status, "id": container_id})
        if cur.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Container not found")
    conn.commit()
    return {"container_id": container_id, "status": status}

@router.delete("/{container_id}")
def delete_container(container_id: str, conn: oracledb.Connection = Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM containers WHERE id = :id", {"id": container_id})
        if cur.rowcount == 0:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Container not found")
    conn.commit()
    return {"container_id": container_id, "status": "deleted"}  

@router.post("/{container_id}/gate_out")
def gate_out(container_id: str, conn: oracledb.Connection = Depends(get_conn)):
    try:
        with conn.cursor() as cur:
            result = cur.var(str)
            cur.callproc("pkg_gate.process_gate_out", [container_id, result])
        conn.commit()

    except oracledb.DatabaseError as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Container not found")
    return {"container_id": container_id, "status": result.getvalue()}