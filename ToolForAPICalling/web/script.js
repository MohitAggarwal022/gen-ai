const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");

// Store todos
let todos = [];

// Render todos
function renderTodos() {
    todoList.innerHTML = "";
    todos.forEach((todo, idx) => {
        const li = document.createElement("li");
        li.textContent = todo;

        const delBtn = document.createElement("button");
        delBtn.className = "delete-btn";
        delBtn.innerHTML = "&times;";
        delBtn.onclick = () => {
            deleteTodo(idx);
        };
        li.appendChild(delBtn);
        todoList.appendChild(li);
    });
}

// Add todo
function addTodo(todo) {
    todos.push(todo);
    renderTodos();
}

// Delete todo
function deleteTodo(idx) {
    todos.splice(idx, 1);
    renderTodos();
}

// Handle form submit
todoForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const newTodo = todoInput.value.trim();
    if (newTodo.length > 0) {
        addTodo(newTodo);
        todoInput.value = "";
    }
});

// Initial render
renderTodos();
