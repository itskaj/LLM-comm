// script.js - JavaScript for LLM Communication Framework Documentation

document.addEventListener('DOMContentLoaded', (event) => {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add active class to current nav item
    const currentPage = window.location.pathname.split("/").pop();
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('text-blue-200');
        }
    });

    // Add copy to clipboard functionality for code snippets (if any)
    document.querySelectorAll('pre code').forEach((block) => {
        const button = document.createElement('button');
        button.innerText = 'Copy';
        button.classList.add('absolute', 'top-2', 'right-2', 'bg-gray-700', 'text-white', 'px-2', 'py-1', 'rounded', 'text-sm');
        
        block.parentNode.style.position = 'relative';
        block.parentNode.appendChild(button);

        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.innerText);
            button.innerText = 'Copied!';
            setTimeout(() => {
                button.innerText = 'Copy';
            }, 2000);
        });
    });
});