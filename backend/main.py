from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import session, engine
from models import Todo, Base

Base.metadata.create_all(bind= engine) # kod çalışmadan önce veritabanında gerekli tabloları oluşturur

app = FastAPI()

# api izin ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # güvenlik için localhostu veriyoruz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db(): # her bir fonksiyonda veritabanı bağlantısı açılıp kapatılacak
    db = session # veritabanı bağlantısı oluşturur
    try:
        yield db # veritabanını getir
    finally:
        db.close() # bağlantıyı kapat 

@app.get("/")
def root():
    return {"id": "1", "todo": "content"}

@app.get("/todos")
def get_all_todos(db = Depends(get_db)): # db = Depends(get_db) db bağlantısı açar
    todos = db.query(Todo).all() # tüm todo tablosunu getir
    if todos == []:
        return {"message": "Bir gorev ekleyin.", "todos": todos}
    return {"message": "Görevler başarıyla yüklendi!", "todos": todos}

class TodoCreate(BaseModel): #  bu tipde veri gelirse kayıt yapılır
    content: str

@app.post("/todos")
def create_todo(newTodo: TodoCreate ,db = Depends(get_db)):
    db_newTodo = Todo(content = newTodo.content) 
    db.add(db_newTodo) # veritabanına ekleme
    db.commit() # veritabanına kayıt etme 
    db.refresh(db_newTodo)  # Veritabanındaki yeni kaydın verilerini almak için refresh() kullaniyoruz
    return {"message": f"'{db_newTodo.content}' gorevi eklendi.", "todo": {"id": db_newTodo.id, "content": db_newTodo.content}}


class TodoUpdate(BaseModel): #  bu tipde veri gelmesini bekliyoruz
    content: str

@app.put("/todos/{id}")
def update_todo(id: int, Updated_todo: TodoUpdate, db = Depends(get_db)):
    todo_item = db.query(Todo).filter(Todo.id == id).first() # tüm id lerde gelen id yi filtreliyoruz ve değişkene alıyoruz
    if not todo_item: # id icin veritabaninda eslesme yoksa
        raise HTTPException(status_code=404, detail="Todo Bulunamadı!")  # hata gönderiyoruz
    
    todo_item.content = Updated_todo.content # varolan todo içeriğine gelen içeriği atıyoruz
    db.add(todo_item)
    db.commit()
    return {"message": "Görev başarıyla güncellendi."}

@app.delete("/todos/{id}")
def update_todo(id: int, db = Depends(get_db)):
    todo_item = db.query(Todo).filter(Todo.id == id).first() # id ye göre filtreleme
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo Bulunamadı!")
    
    db.delete(todo_item)
    db.commit()
    return {"message": f"'{todo_item.content}' görevi silindi."}