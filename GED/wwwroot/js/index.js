document.addEventListener('DOMContentLoaded', function () {
    const basePath = window.basePath; // Use global variable
    const tableContent = document.getElementById('tableContent');
    const tableLoader = document.getElementById('tableLoader');
    const searchInput = document.getElementById('searchInput');
    const clearButton = document.getElementById('clearButton');
    const searchButton = document.getElementById('searchButton');

    let isLoading = false;

    function showLoader() {
        if (!isLoading) {
            isLoading = true;
            tableLoader.style.display = 'flex';
            tableContent.classList.add('blurred');
        }
    }

    function hideLoader() {
        isLoading = false;
        tableLoader.style.display = 'none';
        tableContent.classList.remove('blurred');
    }

    function updateClearVisibility() {
        if (searchInput.value.trim() === '') {
            clearButton.classList.add('hidden-element');
        } else {
            clearButton.classList.remove('hidden-element');
        }
    }

    function loadPlans(url, pushHistory = true) {
        // Prevent multiple simultaneous requests
        if (isLoading) return;

        showLoader();

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            tableContent.innerHTML = data;
            if (pushHistory) {
                const state = { 'source': 'ajax' };
                window.history.pushState(state, '', url);
            }
        })
        .catch(error => {
            console.error('Error loading plans:', error);
            alert("Erreur lors du chargement des plans.");
        })
        .finally(() => {
            hideLoader();
        });
    }

    // Initialize
    updateClearVisibility();

    let typingTimer;
    const TYPING_DELAY = 300;

    // Search input with debounce
    searchInput.addEventListener('input', function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function() {
            const term = searchInput.value.trim();
            const url = term === '' ? basePath : `${basePath}?searchTerm=${encodeURIComponent(term)}&page=1`;
            loadPlans(url);
            updateClearVisibility();
        }, TYPING_DELAY);
    });

    // Enter key search
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            clearTimeout(typingTimer);
            const term = searchInput.value.trim();
            const url = term === '' ? basePath : `${basePath}?searchTerm=${encodeURIComponent(term)}&page=1`;
            loadPlans(url);
            updateClearVisibility();
        }
    });

    // Search button click
    searchButton.addEventListener('click', function() {
        clearTimeout(typingTimer);
        const term = searchInput.value.trim();
        const url = term === '' ? basePath : `${basePath}?searchTerm=${encodeURIComponent(term)}&page=1`;
        loadPlans(url);
        updateClearVisibility();
    });

    // Clear button
    clearButton.addEventListener('click', function(e) {
        e.preventDefault();
        searchInput.value = '';
        updateClearVisibility();
        loadPlans(basePath, true);
    });

    // Pagination click (event delegation)
    document.addEventListener('click', function(e) {
        if (e.target.matches('.page-link') || e.target.closest('.page-link')) {
            e.preventDefault();
            const pageLink = e.target.matches('.page-link') ? e.target : e.target.closest('.page-link');
            const url = pageLink.getAttribute('href');
            if (url && url !== '#') {
                loadPlans(url);
            }
        }
    });

    // Handle browser back/forward
    window.addEventListener('popstate', function(event) {
        if (event.state && event.state.source === 'ajax') {
            loadPlans(location.href, false);
        }
    });
});