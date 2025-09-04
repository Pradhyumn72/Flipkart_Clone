 // Password toggle functionality
 function togglePassword() {
    const passwordField = document.getElementById('password');
    const toggleBtn = document.querySelector('.password-toggle i');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleBtn.className = 'fas fa-eye-slash';
    } else {
        passwordField.type = 'password';
        toggleBtn.className = 'fas fa-eye';
    }
}

// Form submission handling
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const adminId = document.getElementById('adminId').value;
    const password = document.getElementById('password').value;
    
    // Show loading overlay
    document.getElementById('loadingOverlay').style.display = 'flex';
    
    // Simulate login process
    setTimeout(function() {
        document.getElementById('loadingOverlay').style.display = 'none';
        
        // Demo credentials check
        if ((adminId === 'admin' || adminId === 'admin@flipkart.com') && password === 'admin123') {
            alert('✅ Login Successful!\n\nWelcome to Flipkart Admin Dashboard!\n\nIn a real application, you would be redirected to the main admin dashboard with features like:\n\n• Product Management\n• Order Management\n• User Management\n• Analytics & Reports\n• Seller Management\n• Inventory Control');
        } else {
            alert('❌ Login Failed!\n\nPlease use demo credentials:\nUsername: admin (or admin@flipkart.com)\nPassword: admin123');
        }
    }, 2000);
});

// Add some interactive effects
document.addEventListener('DOMContentLoaded', function() {
    // Add focus effects to form inputs
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });

    // Quick access button interactions
    const quickBtns = document.querySelectorAll('.quick-btn');
    quickBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const btnText = this.textContent.trim();
            alert(`🚀 ${btnText} feature would be available in the full implementation!`);
        });
    });

    // Forgot password link
    document.querySelector('.forgot-password').addEventListener('click', function(e) {
        e.preventDefault();
        alert('🔑 Password Reset\n\nIn a real application, this would send a password reset link to your registered email address.');
    });

    // Add demo info on page load
    setTimeout(function() {
        console.log('%c🎯 Flipkart Admin Login Demo', 'color: #047BD5; font-size: 16px; font-weight: bold;');
        console.log('Demo Credentials:');
        console.log('Username: admin (or admin@flipkart.com)');
        console.log('Password: admin123');
    }, 1000);
});

// Add some dynamic stats animation
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach((stat, index) => {
        setTimeout(() => {
            stat.style.animation = 'pulse 0.6s ease';
        }, index * 200);
    });
}

// Animate stats on page load
window.addEventListener('load', () => {
    setTimeout(animateStats, 1000);
    setInterval(animateStats, 10000); // Repeat every 10 seconds
});

// Add CSS for pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);