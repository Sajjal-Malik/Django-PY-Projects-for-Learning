import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({
    title: "",
    description: ""
  });

  // Load tasks from the backend
  const fetchTasks = () => {
    axios.get("/api/tasks/")
      .then(res => setTasks(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Create a new task
  const handleCreate = (e) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;

    axios.post("/api/tasks/", newTask)
      .then(() => {
        fetchTasks();  // Refresh the list
        setNewTask({ title: "", description: "" });  // Clear form
      })
      .catch(err => console.error(err));
  };

  const handleToggleComplete = (task) => {
    axios.put(`/api/tasks/${task.id}/`, {
      ...task,
      completed: !task.completed,
    })
      .then(() => fetchTasks())
      .catch(err => console.error(err));
  };


  return (
    <div style={{ padding: "20px" }}>
      <h1>Task List</h1>

      <form onSubmit={handleCreate} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Task Title"
          value={newTask.title}
          onChange={e => setNewTask({ ...newTask, title: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={newTask.description}
          onChange={e => setNewTask({ ...newTask, description: e.target.value })}
        />
        <button type="submit">Add Task</button>
      </form>

      <ul>
        {tasks.map(task => (
          <li key={task.id} style={{ marginBottom: "10px" }}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => handleToggleComplete(task)}
              style={{ marginRight: "10px" }}
            />
            <strong>{task.title}</strong>
            {task.description && <> — <em>{task.description}</em></>}
          </li>
        ))}
      </ul>
    </div>
  );

}

export default App;
