function login() {
    // Get the selected user type from the dropdown
    const userType = document.getElementById("userType").value;
    const message = document.getElementById("message");

    // Redirect based on the selected user type
    switch (userType) {
        case "customer":
            // Use the correct route
            window.location.href = "/customer_login_page";
            break;
        case "hotelOwner":
            // Use the correct route
            window.location.href = "/hotel_login_page";
            break;
        case "inspector":
            // Use the correct route
            window.location.href = "/inspector_login_page";
            break;
        default:
            message.textContent = "Please select a valid user type.";
    }
}