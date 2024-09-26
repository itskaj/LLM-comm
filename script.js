document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const sideNav = document.getElementById('side-nav');
    const links = document.querySelectorAll('a[href^="#"]');
    
    // Toggle mobile menu
    menuToggle.addEventListener('click', () => {
        sideNav.classList.toggle('active');
    });

    // Smooth scrolling and active link highlighting
    links.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            window.scrollTo({
                top: targetElement.offsetTop - 20,
                behavior: 'smooth'
            });

            // Close mobile menu if open
            sideNav.classList.remove('active');

            // Update active link
            links.forEach(l => l.classList.remove('active-link'));
            link.classList.add('active-link');
        });
    });

    // Intersection Observer for section highlighting
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                links.forEach(link => {
                    link.classList.toggle('active-link', link.getAttribute('href') === `#${id}`);
                });
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('section[id]').forEach(section => {
        observer.observe(section);
    });

    // Show/hide side navigation based on scroll position
    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {
        const st = window.pageYOffset || document.documentElement.scrollTop;
        if (st > lastScrollTop && st > 100) {
            // Scrolling down
            sideNav.classList.add('md:hidden');
        } else {
            // Scrolling up
            sideNav.classList.remove('md:hidden');
        }
        lastScrollTop = st <= 0 ? 0 : st;
    }, false);
});