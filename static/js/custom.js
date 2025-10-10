// Custom JavaScript for RentaCar System

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Loading animation for buttons
    function showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="loading me-2"></span>Loading...';
        button.disabled = true;
        
        return function() {
            button.innerHTML = originalText;
            button.disabled = false;
        };
    }

    // Car search functionality
    const searchForm = document.getElementById('car-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const resetLoading = showButtonLoading(submitBtn);
            
            // Reset loading after form submission
            setTimeout(resetLoading, 2000);
        });
    }

    // Filter functionality
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('input, select');
        
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Auto-submit form when filters change
                filterForm.submit();
            });
        });
    }

    // Car availability checker
    function checkCarAvailability(carId, pickupDate, returnDate) {
        const url = `/api/cars/${carId}/availability/?pickup_date=${pickupDate}&return_date=${returnDate}`;
        
        return fetch(url)
            .then(response => response.json())
            .then(data => {
                return data.available;
            })
            .catch(error => {
                console.error('Error checking availability:', error);
                return false;
            });
    }

    // Book car functionality
    const bookButtons = document.querySelectorAll('.btn-book-car');
    bookButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const carId = this.dataset.carId;
            const carName = this.dataset.carName;
            const dailyRate = this.dataset.dailyRate;
            
            // Show booking modal or redirect to booking page
            showBookingModal(carId, carName, dailyRate);
        });
    });

    // Booking modal functionality
    function showBookingModal(carId, carName, dailyRate) {
        const modalHtml = `
            <div class="modal fade" id="bookingModal" tabindex="-1" aria-labelledby="bookingModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="bookingModalLabel">
                                <i class="bi bi-calendar-check me-2"></i>Book ${carName}
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form id="booking-form">
                                <div class="row">
                                    <div class="col-md-6">
                                        <label for="pickup-date" class="form-label">Pickup Date</label>
                                        <input type="datetime-local" class="form-control" id="pickup-date" required>
                                    </div>
                                    <div class="col-md-6">
                                        <label for="return-date" class="form-label">Return Date</label>
                                        <input type="datetime-local" class="form-control" id="return-date" required>
                                    </div>
                                </div>
                                <div class="row mt-3">
                                    <div class="col-md-12">
                                        <div class="card bg-light">
                                            <div class="card-body">
                                                <h6>Pricing Details</h6>
                                                <div class="d-flex justify-content-between">
                                                    <span>Daily Rate:</span>
                                                    <span class="fw-bold">$${dailyRate}/day</span>
                                                </div>
                                                <div class="d-flex justify-content-between">
                                                    <span>Duration:</span>
                                                    <span id="rental-duration">0 days</span>
                                                </div>
                                                <hr>
                                                <div class="d-flex justify-content-between">
                                                    <span class="fw-bold">Total:</span>
                                                    <span class="fw-bold text-primary" id="total-price">$0.00</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-3">
                                    <label for="special-requests" class="form-label">Special Requests</label>
                                    <textarea class="form-control" id="special-requests" rows="3" placeholder="Any special requests or notes..."></textarea>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" id="confirm-booking">
                                <i class="bi bi-check-circle me-2"></i>Confirm Booking
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('bookingModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
        modal.show();

        // Add event listeners for the modal
        const pickupInput = document.getElementById('pickup-date');
        const returnInput = document.getElementById('return-date');
        const durationSpan = document.getElementById('rental-duration');
        const totalPriceSpan = document.getElementById('total-price');

        function updatePricing() {
            const pickupDate = new Date(pickupInput.value);
            const returnDate = new Date(returnInput.value);
            
            if (pickupDate && returnDate && returnDate > pickupDate) {
                const diffTime = Math.abs(returnDate - pickupDate);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                const totalPrice = diffDays * parseFloat(dailyRate);
                
                durationSpan.textContent = `${diffDays} day${diffDays !== 1 ? 's' : ''}`;
                totalPriceSpan.textContent = `$${totalPrice.toFixed(2)}`;
            } else {
                durationSpan.textContent = '0 days';
                totalPriceSpan.textContent = '$0.00';
            }
        }

        pickupInput.addEventListener('change', updatePricing);
        returnInput.addEventListener('change', updatePricing);

        // Set minimum dates to today
        const today = new Date();
        const todayString = today.toISOString().slice(0, 16);
        pickupInput.min = todayString;
        returnInput.min = todayString;

        // Update return date minimum when pickup date changes
        pickupInput.addEventListener('change', function() {
            returnInput.min = this.value;
        });

        // Handle booking confirmation
        document.getElementById('confirm-booking').addEventListener('click', function() {
            const pickupDate = pickupInput.value;
            const returnDate = returnInput.value;
            const specialRequests = document.getElementById('special-requests').value;

            if (!pickupDate || !returnDate) {
                alert('Please select both pickup and return dates.');
                return;
            }

            if (new Date(returnDate) <= new Date(pickupDate)) {
                alert('Return date must be after pickup date.');
                return;
            }

            // Show loading
            const resetLoading = showButtonLoading(this);

            // Check availability first
            checkCarAvailability(carId, pickupDate, returnDate)
                .then(available => {
                    if (available) {
                        // Simulate booking process
                        setTimeout(() => {
                            alert(`Booking confirmed for ${carName}!\\nPickup: ${pickupDate}\\nReturn: ${returnDate}`);
                            modal.hide();
                            resetLoading();
                        }, 1500);
                    } else {
                        alert('Sorry, this car is not available for the selected dates.');
                        resetLoading();
                    }
                });
        });
    }

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('loading');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Search suggestions
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    fetchSearchSuggestions(query);
                }, 300);
            } else {
                hideSearchSuggestions();
            }
        });
    }

    function fetchSearchSuggestions(query) {
        fetch(`/api/cars/?search=${query}&limit=5`)
            .then(response => response.json())
            .then(data => {
                showSearchSuggestions(data.results);
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
    }

    function showSearchSuggestions(cars) {
        const suggestionsContainer = document.getElementById('search-suggestions');
        if (!suggestionsContainer) return;

        const suggestionsHtml = cars.map(car => `
            <div class="suggestion-item p-2 border-bottom" data-car-id="${car.id}">
                <div class="d-flex align-items-center">
                    <i class="bi bi-car-front me-2"></i>
                    <div>
                        <div class="fw-bold">${car.full_name}</div>
                        <small class="text-muted">$${car.daily_rate}/day</small>
                    </div>
                </div>
            </div>
        `).join('');

        suggestionsContainer.innerHTML = suggestionsHtml;
        suggestionsContainer.style.display = 'block';

        // Add click handlers
        suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', function() {
                const carId = this.dataset.carId;
                window.location.href = `/cars/${carId}/`;
            });
        });
    }

    function hideSearchSuggestions() {
        const suggestionsContainer = document.getElementById('search-suggestions');
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
    }

    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        const searchContainer = document.querySelector('.search-container');
        if (searchContainer && !searchContainer.contains(e.target)) {
            hideSearchSuggestions();
        }
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Export functions for global access
window.RentaCar = {
    checkCarAvailability,
    formatCurrency,
    formatDate
};