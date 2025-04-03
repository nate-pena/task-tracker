// Update API URL to use the exposed backend URL
const API_BASE_URL = 'https://8000-ijisytdyzm5mm903xr1nd-226a4af3.manus.computer';

// API Integration Functions
async function fetchTasksFromBackend() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/tasks`);
        if (response.ok) {
            const data = await response.json();
            tasks = data;
            saveTasksToStorage();
            renderTasks();
            updateTaskCount();
        }
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

async function sendTaskToBackend(task) {
    try {
        await fetch(`${API_BASE_URL}/api/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task),
        });
    } catch (error) {
        console.error('Error adding task:', error);
    }
}

async function updateTaskInBackend(task) {
    try {
        await fetch(`${API_BASE_URL}/api/tasks/${task.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task),
        });
    } catch (error) {
        console.error('Error updating task:', error);
    }
}

async function deleteTaskFromBackend(id) {
    try {
        await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
            method: 'DELETE',
        });
    } catch (error) {
        console.error('Error deleting task:', error);
    }
}
