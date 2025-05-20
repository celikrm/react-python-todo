import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

const url = "http://localhost:8000"; // URL'yi tanımlıyoruz

function App() {
  const [newTodo, setNewTodo] = useState(""); // Todo'yu state olarak tutuyoruz
  const [todos, setTodos] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState(" ");
  const [editContent, setEditContent] = useState("");

  // --------------------------Todo oluşturma
  const handleCreateTodo = async () => {
    if (!newTodo) return; //false, null, undefined, 0, NaN, veya "" (boş string) ise fonksiyonu sonlandir
    try {
      // API'den veri alıyoruz
      const response = await axios.post(`${url}/todos`, { content: newTodo });
      console.log(response.data); // Gelen veriyi konsola yazdırıyoruz
      get_todos_update();
      setMessage(response.data.message); // Backend den gelen mesajı yazdırıyoruz
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      const errMsg = error.response?.data?.detail || "Bir hata oluştu!"; // backenden hata mesajını alıyoruz
      setMessage(errMsg);
      setTimeout(() => setMessage(""), 3000);
    }
  };

  // --------------------------Todo Listeleme
  const get_todos = async () => {
    await axios.get(`${url}/todos`).then((response) => {
      setTodos(response.data.todos);
      console.log(response.data.todos);
      setMessage(response.data.message);
      setTimeout(() => setMessage(""), 3000);
    });
  };
  const get_todos_update = async () => {
    await axios.get(`${url}/todos`).then((response) => {
      setTodos(response.data.todos);
    });
  };

  // --------------------------Todo Silme
  const delete_todo = async (id) => {
    if (!window.confirm("Gorev silinsin mi?")) return;
    try {
      const response = await axios.delete(`${url}/todos/${id}`);
      setMessage(response.data.message); // backenden gelen mesaj
      setTimeout(() => setMessage(""), 5000);
      get_todos_update();
    } catch (error) {
      const errMsg = error.response?.data?.detail || "Silme işleminde hata!";
      setMessage(errMsg);
      setTimeout(() => setMessage(""), 5000);
    }
  };

  // --------------------------Todo Güncelleme
 const update_todo = async (todo_id) => {
  try {
    const res = await axios.put(`${url}/todos/${todo_id}`, { content: editContent });
    get_todos_update();
    setMessage(res.data.message);
    setTimeout(() => setMessage(""), 3000);
  } catch (error) {
    const errMsg = error.response?.data?.detail || "Bir hata oluştu!";
    setMessage(errMsg);
    setTimeout(() => setMessage(""), 3000);
  }
};
  //Başlangıçta tüm todolari getir
  useEffect(() => {
    get_todos();
  }, []);

  return (
    <div>
      <h1>Todo App</h1>
      <div className="todo-ekle">
        <div style={{ height: "24px" }}>{message && <h4>{message}</h4>}</div>
        <input
          placeholder="Gorev ekle"
          className="todo-ekle-input"
          type="text"
          value={newTodo}
          onChange={(e) => {
            setNewTodo(e.target.value);
            setEditingId(null);
          }}
        />
        <button onClick={handleCreateTodo}>Ekle</button>{" "}
      </div>
      <div>
        <ul>
          {todos.map((todo) => (
            <li key={todo.id} className="todo-item">
              <form onSubmit={(e) => update_todo(todo.id, e)}>
                <input
                  value={editingId === todo.id ? editContent : todo.content}
                  disabled={editingId !== todo.id}
                  onChange={(e) => setEditContent(e.target.value)}
                  className={
                    editingId === todo.id ? "input-active" : "input-disabled"
                  }
                />
                <>
                  {editingId === todo.id ? (
                    <button
                      type="button"
                      onClick={() => {
                        update_todo(todo.id);
                        setEditingId(null);
                      }}
                    >
                      Kaydet
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={() => {
                        setEditingId(todo.id);
                        setEditContent(todo.content);
                      }}
                    >
                      Düzenle
                    </button>
                  )}
                  <button type="button" onClick={() => delete_todo(todo.id)}>
                    Sil
                  </button>
                </>
                <hr />
              </form>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;

