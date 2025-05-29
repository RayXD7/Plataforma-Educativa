document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePassword = document.querySelector('.toggle-password');
    const passwordField = document.querySelector('#password');
    
    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle eye icon
            const eyeIcon = this.querySelector('i');
            eyeIcon.classList.toggle('fa-eye');
            eyeIcon.classList.toggle('fa-eye-slash');
        });
    }
    
    // Form validation visual feedback
    const loginForm = document.querySelector('.login-form');
    const formInputs = document.querySelectorAll('.form-control');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            formInputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
        
        formInputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    }
    
    // Add subtle animation to the login card on hover
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        loginCard.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element
            const y = e.clientY - rect.top;  // y position within the element
            
            // Calculate rotation based on mouse position
            // The rotation will be subtle, max 2 degrees
            const rotateX = (y / rect.height - 0.5) * -4;
            const rotateY = (x / rect.width - 0.5) * 4;
            
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
        });
        
        loginCard.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
        });
    }
    
    // Add focus effect to input groups
    const inputGroups = document.querySelectorAll('.input-group');
    inputGroups.forEach(group => {
        const input = group.querySelector('.form-control');
        const icon = group.querySelector('.input-group-text i');
        
        if (input && icon) {
            input.addEventListener('focus', function() {
                icon.style.color = 'var(--primary-color)';
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    icon.style.color = '';
                }
            });
        }
    });
});