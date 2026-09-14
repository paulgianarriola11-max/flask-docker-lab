const API_URL = "/items";


// =========================
// LOAD ITEMS
// =========================

async function loadItems() {
    try {
        const response = await fetch(API_URL);
        const items = await response.json();

        const container = document.getElementById("items");
        container.innerHTML = "";

        if (items.length === 0) {
            container.innerHTML = "<p>No items found.</p>";
            return;
        }

        items.forEach(item => {
            const div = document.createElement("div");
            div.className = "item";

            div.innerHTML = `
                <span>${item.name}</span>
                <button class="delete" onclick="deleteItem('${item._id}')">
                    Delete
                </button>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        console.error(error);
        alert("Failed to load items.");
    }
}


// =========================
// ADD ITEM
// =========================

async function addItem() {
    const input = document.getElementById("itemName");
    const name = input.value.trim();

    if (!name) {
        alert("Please enter an item name.");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name
            })
        });

        if (!response.ok) {
            throw new Error("Failed to add item");
        }

        input.value = "";
        await loadItems();

    } catch (error) {
        console.error(error);
        alert("Failed to add item.");
    }
}


// =========================
// DELETE ITEM
// =========================

async function deleteItem(id) {
    try {
        const response = await fetch(`/items/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete item");
        }

        await loadItems();

    } catch (error) {
        console.error(error);
        alert("Failed to delete item.");
    }
}


// =========================
// REGISTER
// =========================

async function register() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const message = document.getElementById("authMessage");

    if (!username || !password) {
        message.textContent = "Please enter a username and password.";
        return;
    }

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.error || "Registration failed.";
            return;
        }

        message.textContent = "Registration successful! You can now login.";

        document.getElementById("password").value = "";

    } catch (error) {
        console.error(error);
        message.textContent = "Unable to connect to the server.";
    }
}


// =========================
// LOGIN
// =========================

async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const message = document.getElementById("authMessage");

    if (!username || !password) {
        message.textContent = "Please enter a username and password.";
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.error || "Login failed.";
            return;
        }

        message.textContent = "Login successful!";

        console.log("Logged in user:", data.user_id);

    } catch (error) {
        console.error(error);
        message.textContent = "Unable to connect to the server.";
    }
}


// =========================
// INITIAL LOAD
// =========================

loadItems();