// ============================================
// Stainy Henna — Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {

    // ---- Initialize AOS ----
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50,
        });
    }

    // ---- Mobile Menu Toggle ----
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            if (mobileMenu.classList.contains('hidden')) {
                menuIcon.classList.remove('fa-times');
                menuIcon.classList.add('fa-bars');
            } else {
                menuIcon.classList.remove('fa-bars');
                menuIcon.classList.add('fa-times');
            }
        });

        // Close mobile menu when clicking a link
        mobileMenu.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
                menuIcon.classList.remove('fa-times');
                menuIcon.classList.add('fa-bars');
            });
        });
    }

    // ---- Navbar Scroll Effect ----
    const navbar = document.getElementById('main-navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // ---- Auto-dismiss Messages ----
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        const alerts = messageContainer.querySelectorAll('.message-alert');
        alerts.forEach(function(alert, index) {
            // Stagger the slide-in animation
            alert.style.animationDelay = (index * 0.15) + 's';

            // Auto-dismiss after 5 seconds
            setTimeout(function() {
                alert.style.transition = 'all 0.5s ease-out';
                alert.style.transform = 'translateX(120%)';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 500);
            }, 5000 + (index * 500));
        });
    }

    // ---- Smooth scroll for anchor links ----
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ---- Add to Cart Animation ----
    document.querySelectorAll('a[href*="cart/add"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            // Add a brief scale animation
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // ---- Active nav link highlight ----
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function(link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('text-maroon-500', 'bg-maroon-50');
            link.classList.remove('text-gray-700');
        }
    });

});
