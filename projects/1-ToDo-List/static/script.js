// Add Task
document.getElementById("addTaskForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let formData = new FormData(this);
    fetch("/add", { method: "POST", body: formData })
        .then(res => res.json())
        .then(() => location.reload());
});

// Drag & Drop using SortableJS
["todo", "progress", "done"].forEach(columnId => {
    new Sortable(document.getElementById(columnId), {
        group: "tasks",
        animation: 150,
        onEnd: function (evt) {
            let taskId = evt.item.dataset.id;
            let newStatus = evt.to.id === "todo" ? "To Do" :
                            evt.to.id === "progress" ? "In Progress" : "Done";

            fetch("/update_status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ task_id: taskId, status: newStatus })
            });
        }
    });
});
