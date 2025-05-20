# SQLAlchemy kütüphanesinden gerekli bileşenleri import ediyoruz
from sqlalchemy import Column, Integer, String, create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker

#  `Base` tüm veritabanı modelleri (class'ları) için temel sınıf
Base = declarative_base()

# Veritabanı bağlantısı
# # SQLite kullanıyoruz ve veritabanının adını belirtiyoruz. 
# # check_same_thread=False, SQLite'ın birden fazla thread tarafından kullanılmasına izin verir.
engine = create_engine('sqlite:///./veritabani.db', connect_args={'check_same_thread': False})

# veritabanıyla etkileşim. 
# `sessionmaker`, SQLAlchemy'nin oturum yönetimi (session) sınıfını oluşturur.
# `autocommit=False`komutu, otomatik commit işlemini kapatir. Yani, veri kaydi icin commit edilmesi gerekir.
# `autoflush=False`, her veri eklemesi (flush) işlemi yapıldığında otomatik olarak veritabanına gönderilmesini engeller.
Session = sessionmaker(autocommit= False, bind=engine, autoflush= False)

session = Session()

