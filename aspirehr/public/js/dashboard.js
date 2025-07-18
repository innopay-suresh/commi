// aspirehr/public/js/dashboard.js

document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.toggle-button');
    const welcomeButton = document.querySelector('.toggle-button .welcome');
    const dashboardButton = document.querySelector('.toggle-button .dashboard');
    const welcomeMessageElement = document.querySelector('.header .welcome-message h2');
    const dashboardCards = document.querySelectorAll('.dashboard-card');

    // Sidebar interactivity (Example: Toggle on click)
    // You might need a button to trigger this or adjust based on floating requirement
    // For a floating sidebar that appears on hover, CSS would be more appropriate.
    // This is a basic toggle example.
    // Example: Add a button in HTML with class 'sidebar-toggle'
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open'); // Requires CSS for .sidebar.open
        });
    }


    // Navigation for sidebar menu items
    const menuItems = document.querySelectorAll('.sidebar-menu .menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default link behavior
            const route = item.getAttribute('data-route');
            if (route) {
                frappe.set_route(route);
            }
        });
    });

    // Navigation for dashboard cards
    dashboardCards.forEach(card => {
        card.addEventListener('click', () => {
            const route = card.getAttribute('data-route');
            if (route) {
                frappe.set_route(route);
            }
        });
    });

    // Toggle button functionality (Visual indication)
    if (toggleButton && welcomeButton && dashboardButton) {
        welcomeButton.addEventListener('click', () => {
            welcomeButton.classList.add('active');
            dashboardButton.classList.remove('active');
            // Add logic to show Welcome content
        });

        dashboardButton.addEventListener('click', () => {
            dashboardButton.classList.add('active');
            welcomeButton.classList.remove('active');
            // Add logic to show Dashboard content
        });

        // Set initial active state (e.g., based on current view)
        // welcomeButton.classList.add('active'); // Assuming Welcome is default
    }

    // Fetch user information and display welcome message (Example using Frappe.call)
    // This assumes you have a server-side method like 'get_user_fullname'
    // if (welcomeMessageElement) {
    //     frappe.call({
    //         method: 'frappe.get_user_fullname', // Replace with your actual method
    //         callback: function(r) {
    //             if (r.message) {
    //                 const now = new Date();
    //                 const hour = now.getHours();
    //                 let greeting = 'Good Evening';
    //                 if (hour < 12) {
    //                     greeting = 'Good Morning';
    //                 } else if (hour < 18) {
    //                     greeting = 'Good Afternoon';
    //                 }
    //                 welcomeMessageElement.textContent = `${greeting}, ${r.message} 👋`;
    //             }
    //         }
    //     });
    // }

    // Basic animation for card entrance
    if (dashboardCards.length > 0) {
        dashboardCards.forEach((card, index) => {
            card.style.opacity = 0;
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                card.style.opacity = 1;
                card.style.transform = 'translateY(0)';
            }, index * 100); // Stagger the animation
        });
    }
});