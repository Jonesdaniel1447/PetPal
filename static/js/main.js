// PetPal Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize photo preview
    initializePhotoPreview();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize auto-hide alerts
    initializeAutoHideAlerts();
    
    // Initialize weight chart updates
    initializeWeightCharts();
    
    // Initialize confirmation dialogs
    initializeConfirmations();
    
    // Add loading states to forms
    initializeLoadingStates();
    
    // Initialize keyboard navigation
    initializeKeyboardNavigation();
    
    // Initialize pet-themed features
    initializePetThemeFeatures();
    
    // Initialize dynamic content
    initializeDynamicContent();
    
    console.log('PetPal JavaScript initialized successfully!');
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Enhanced form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Real-time validation for specific fields
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('blur', validateEmail);
    });
    
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        field.addEventListener('input', validatePassword);
    });
}

// Email validation
function validateEmail(event) {
    const email = event.target.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        event.target.setCustomValidity('Please enter a valid email address');
    } else {
        event.target.setCustomValidity('');
    }
}

// Password validation
function validatePassword(event) {
    const password = event.target.value;
    const minLength = 6;
    
    if (password.length > 0 && password.length < minLength) {
        event.target.setCustomValidity(`Password must be at least ${minLength} characters long`);
    } else {
        event.target.setCustomValidity('');
    }
    
    // Check for confirm password field
    const confirmField = document.querySelector('input[name="confirm_password"]');
    if (confirmField && confirmField.value) {
        if (password !== confirmField.value) {
            confirmField.setCustomValidity('Passwords do not match');
        } else {
            confirmField.setCustomValidity('');
        }
    }
}

// Photo preview functionality
function initializePhotoPreview() {
    const photoInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    photoInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                // Check file size (16MB limit)
                const maxSize = 16 * 1024 * 1024;
                if (file.size > maxSize) {
                    showAlert('File size must be less than 16MB', 'danger');
                    event.target.value = '';
                    return;
                }
                
                // Check file type
                if (!file.type.startsWith('image/')) {
                    showAlert('Please select a valid image file', 'danger');
                    event.target.value = '';
                    return;
                }
                
                // Create preview
                createImagePreview(file, input);
            }
        });
    });
}

// Create image preview
function createImagePreview(file, input) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Remove existing preview
        const existingPreview = input.parentNode.querySelector('.image-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Create new preview
        const preview = document.createElement('div');
        preview.className = 'image-preview mt-2';
        preview.innerHTML = `
            <img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px; max-height: 200px;" alt="Preview">
            <button type="button" class="btn btn-sm btn-outline-danger ms-2" onclick="removePreview(this)">
                <i data-feather="x"></i> Remove
            </button>
        `;
        
        input.parentNode.insertBefore(preview, input.nextSibling);
        
        // Re-initialize feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    };
    reader.readAsDataURL(file);
}

// Remove image preview
function removePreview(button) {
    const preview = button.closest('.image-preview');
    const input = preview.previousElementSibling;
    
    preview.remove();
    input.value = '';
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Auto-hide alerts after 5 seconds
function initializeAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

// Initialize weight charts with enhanced features
function initializeWeightCharts() {
    const weightCharts = document.querySelectorAll('#weightChart');
    
    weightCharts.forEach(canvas => {
        const petId = canvas.getAttribute('data-pet-id');
        if (petId) {
            loadWeightChartData(petId, canvas);
        }
    });
}

// Load weight chart data via AJAX
function loadWeightChartData(petId, canvas) {
    fetch(`/weight_chart_data/${petId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error loading weight data:', data.error);
                return;
            }
            
            createWeightChart(canvas, data);
        })
        .catch(error => {
            console.error('Error fetching weight data:', error);
        });
}

// Create enhanced weight chart
function createWeightChart(canvas, data) {
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Weight (kg)',
                data: data.data,
                borderColor: 'rgb(74, 144, 226)',
                backgroundColor: 'rgba(74, 144, 226, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: 'rgb(74, 144, 226)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Weight (kg)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgb(74, 144, 226)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Initialize confirmation dialogs
function initializeConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Add loading states to forms
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
                submitButton.disabled = true;
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }, 10000);
            }
        });
    });
}

// Keyboard navigation improvements
function initializeKeyboardNavigation() {
    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
    
    // Enter key to trigger primary actions
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            const primaryButton = document.querySelector('.btn-primary:not([disabled])');
            if (primaryButton) {
                primaryButton.click();
            }
        }
    });
}

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertContainer);
            bsAlert.close();
        }, 5000);
    }
}

// Utility function to format dates
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Utility function to format time
function formatTime(time) {
    return new Date(`1970-01-01T${time}`).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Debounce utility function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Local storage utilities
const storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(`petpal_${key}`, JSON.stringify(value));
        } catch (e) {
            console.warn('Could not save to localStorage:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(`petpal_${key}`);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.warn('Could not read from localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(`petpal_${key}`);
        } catch (e) {
            console.warn('Could not remove from localStorage:', e);
        }
    }
};

// Form data persistence
function initializeFormPersistence() {
    const forms = document.querySelectorAll('form[data-persist]');
    
    forms.forEach(form => {
        const formId = form.getAttribute('data-persist');
        
        // Load saved data
        const savedData = storage.get(`form_${formId}`);
        if (savedData) {
            Object.keys(savedData).forEach(name => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field && field.type !== 'file') {
                    field.value = savedData[name];
                }
            });
        }
        
        // Save data on input
        const saveFormData = debounce(() => {
            const formData = new FormData(form);
            const data = {};
            for (let [name, value] of formData.entries()) {
                if (form.querySelector(`[name="${name}"]`).type !== 'file') {
                    data[name] = value;
                }
            }
            storage.set(`form_${formId}`, data);
        }, 1000);
        
        form.addEventListener('input', saveFormData);
        
        // Clear saved data on successful submit
        form.addEventListener('submit', () => {
            setTimeout(() => {
                storage.remove(`form_${formId}`);
            }, 1000);
        });
    });
}

// Initialize theme switching (if needed in future)
function initializeThemeToggle() {
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            storage.set('theme', newTheme);
        });
        
        // Load saved theme
        const savedTheme = storage.get('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-bs-theme', savedTheme);
        }
    }
}

// Performance monitoring
function initializePerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${Math.round(loadTime)}ms`);
        
        if (loadTime > 3000) {
            console.warn('Page load time is slower than expected');
        }
    });
    
    // Monitor large images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            if (this.naturalWidth > 2000 || this.naturalHeight > 2000) {
                console.warn(`Large image detected: ${this.src}`);
            }
        });
    });
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // In production, you might want to send this to an error tracking service
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // In production, you might want to send this to an error tracking service
});

// Export utilities for use in other scripts
window.PetPal = {
    showAlert,
    formatDate,
    formatTime,
    debounce,
    storage
};
