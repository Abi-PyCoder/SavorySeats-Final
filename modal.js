document.addEventListener("DOMContentLoaded", function() {
    const openModalBtn = document.getElementById("open-modal");
    const modal = document.getElementById("myModal{{food.id}}");
    const closeModalBtn = document.getElementById("close-modal");
    const plusButton = document.querySelector(".plus");
    const minusButton = document.querySelector(".minus")

    // Open the modal
    openModalBtn.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent the default link behavior
        modal.style.display = "block";
    });

    // Close the modal
    closeModalBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Close the modal if the background is clicked
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // Prevent the modal from closing when clicking the plus or minus button
    plusButton.addEventListener("click", function(event) {
        event.preventDefault();
        event.stopPropagation();
    });

    minusButton.addEventListener("click", function(event) {
        event.preventDefault();
        event.stopPropagation();
    });
});