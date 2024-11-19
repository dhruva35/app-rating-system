// Handle search functionality
function searchApps() {
    const query = document.getElementById('searchInput').value;
    if (query.length < 2) return;

    fetch(`/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(apps => {
            updateAppGrid(apps);
            document.querySelector('#mainContent h2').innerHTML = '<i class="fas fa-search"></i> Search Results';
        });
}

// Handle category selection
function loadCategory(category) {
    fetch(`/category/${encodeURIComponent(category)}`)
        .then(response => response.json())
        .then(apps => {
            updateAppGrid(apps);
            document.querySelector('#mainContent h2').innerHTML = `<i class="fas fa-th-large"></i> ${category} Apps`;
        });
}

// Create star rating HTML
function createStarRating(rating) {
    let stars = '';
    for (let i = 0; i < 5; i++) {
        if (i < Math.floor(rating)) {
            stars += '<i class="fas fa-star text-warning"></i>';
        } else if (i < rating) {
            stars += '<i class="fas fa-star-half-alt text-warning"></i>';
        } else {
            stars += '<i class="far fa-star text-warning"></i>';
        }
    }
    return stars;
}

// Format price
function formatPrice(price, priceInr) {
    return price.includes('Free') ? '<span class="text-success">Free</span>' : `₹${priceInr.toFixed(2)}`;
}

// Update the app grid with new data
function updateAppGrid(apps) {
    const appGrid = document.getElementById('appGrid');
    appGrid.innerHTML = '';

    if (!apps || apps.length === 0) {
        appGrid.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info">
                    No apps found matching your criteria.
                </div>
            </div>
        `;
        return;
    }

    apps.forEach(app => {
        const appCard = document.createElement('div');
        appCard.className = 'col-md-4 mb-4';
        appCard.innerHTML = `
            <div class="card h-100">
                <div class="card-body">
                    <div class="app-icon mb-3">
                        <i class="fas fa-mobile-alt fa-3x text-primary"></i>
                    </div>
                    <h5 class="card-title">${app['App Name']}</h5>
                    <span class="category-badge">${app['App Type']}</span>
                    <div class="rating mb-2">
                        <div class="stars">
                            ${createStarRating(app['Average Rating'])}
                        </div>
                        <div class="rating-details">
                            <span class="average-rating">${app['Average Rating'].toFixed(1)}</span>
                            <span class="version-count">(${app['Version Count']} versions)</span>
                            ${app['Highest Rating'] > app['Average Rating'] ? 
                                `<br><small>Best Rating: ${app['Highest Rating'].toFixed(1)}</small>` : ''}
                        </div>
                    </div>
                    <p class="card-text">
                        <strong>Price:</strong> ${formatPrice(app['App Price'], app['Price_INR'])}<br>
                        <strong>Size:</strong> ${app['App Size']}<br>
                        <strong>Downloads:</strong> ${app['Downloads']}<br>
                        <strong>Latest Version:</strong> ${app['Latest Version']}
                    </p>
                </div>
            </div>
        `;
        appGrid.appendChild(appCard);
    });
}

// Add event listener for search input
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchApps();
    }
});
