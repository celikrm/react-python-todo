# react-python-todo

Bu proje, FastAPI kullanılarak oluşturulmuş bir backend ve React (Vite) ile hazırlanmış bir frontend'den oluşmaktadır. Frontend, Axios aracılığıyla backend'e istek gönderir ve gelen verileri kullanıcıya gösterir. Veritabanı olarak SQLite kullanılmıştır.

### Projeyi çalıştırmak için;
**Yüklenmesi gereken paketler**  
cd backend  
pip install -r requirements.txt veya pip install fastapi sqlalchemy uvicorn  
cd ..  
cd frontend  
npm install  

**Uygulamayı Çalıştırma**    
cd frontend  
npm run dev  **(http://localhost:5173/)**   
cd ..  
**(Yeni bir terminal açarak)**  
cd backend  
uvicorn main:app --reload **(http://localhost:8000/)**  
