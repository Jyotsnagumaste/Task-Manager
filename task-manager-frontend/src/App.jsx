import { useEffect, useState } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = () => {
    fetch("http://127.0.0.1:8000/tasks")
      .then((res) => res.json())
      .then((data) => setTasks(data));
  };

  const addTask = () => {
    if (!title) return;

    fetch("http://127.0.0.1:8000/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description: "",
        status: "todo",
      }),
    }).then(() => {
      setTitle("");
      fetchTasks();
    });
  };

  const deleteTask = (id) => {
    fetch(`http://127.0.0.1:8000/tasks/${id}`, {
      method: "DELETE",
    }).then(() => {
      fetchTasks();
    });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Task Manager</h2>

      <input
        placeholder="Enter task title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button onClick={addTask}>Add Task</button>

      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {task.title} — {task.status}
            <button
              onClick={() => deleteTask(task.id)}
              style={{ marginLeft: "10px" }}
            >
              Delete
            </button>
<h1>Hello</h1>

            
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
