document.addEventListener("DOMContentLoaded", function () {
    const emailRows = document.querySelectorAll(".email-row");
    const modal = document.getElementById("emailModal");
    const modalContent = document.getElementById("emailBody");
    const closeModal = document.querySelector(".close");

    emailRows.forEach(row => {
        row.addEventListener("click", function () {
            const uid = this.getAttribute("data-uid");
            modal.style.display = "block";
            modalContent.innerHTML = "Загрузка...";

            // Запрашиваем тело письма через AJAX
            fetch(`/emails/fetch-body?uid=${uid}`)
                .then(response => response.json())
                .then(data => {
                    modalContent.innerHTML = data.body.replace(/\n/g, "<br>");  // Меняем переносы строк
                })
                .catch(error => {
                    modalContent.innerHTML = "Ошибка загрузки письма.";
                    console.error("Ошибка:", error);
                });
        });
    });

    // Закрытие окна
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});
