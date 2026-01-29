const editModal = document.getElementById("editModal");
const editForm = document.getElementById("editExpenseForm");

document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        editModal.classList.remove("hidden");

        document.getElementById("editExpenseId").value = btn.dataset.id;
        document.getElementById("editCategory").value = btn.dataset.category;
        document.getElementById("editAmount").value = btn.dataset.amount;
        document.getElementById("editDate").value = btn.dataset.date;
        document.getElementById("editDescription").value = btn.dataset.description;
    });
});

document.getElementById("closeEditModal").onclick = () => {
    editModal.classList.add("hidden");
};

editForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("expense_id", editExpenseId.value);
    formData.append("category", editCategory.value);
    formData.append("amount", editAmount.value);
    formData.append("date", editDate.value);
    formData.append("description", editDescription.value);
    formData.append("csrfmiddlewaretoken",
        document.querySelector("[name=csrfmiddlewaretoken]").value
    );

    fetch("/expense/edit/ajax/", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const row = document.querySelector(`[data-row="${data.id}"]`);
            row.querySelector(".row-category").innerText = data.category;
            row.querySelector(".row-amount").innerText = "₹ " + data.amount;
            row.querySelector(".row-date").innerText = data.date;
            row.querySelector(".row-description").innerText = data.description;

            editModal.classList.add("hidden");
        }
    });
});
