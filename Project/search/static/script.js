document.getElementById('search-box').addEventListener('input', function() {
    const query = this.value;
    const searchResults = document.getElementById('search-results');
    if (query.length > 0) {
        fetch(`/search/?q=${encodeURIComponent(query)}`) 
            .then(response => response.json())
            .then(data => {
                searchResults.innerHTML = '';
                data.forEach(stock => {
                    const div = document.createElement('div');
                    div.textContent = `${stock.Ticker} - ${stock.Name}`;
                    div.classList.add('stock-item'); 
                    div.dataset.symbol = stock.Ticker; 
                    div.addEventListener('click', () => {
                        fetchStockDetail(stock.Ticker); 
                    });
                    searchResults.appendChild(div);
                });
                searchResults.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
                searchResults.style.display = 'none';
            });
    } else {
        searchResults.style.display = 'none';
    }
});

document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-box').value;
    const searchResults = document.getElementById('search-results');
    if (query.length > 0 && searchResults.childNodes.length > 0) {
        const firstResult = searchResults.childNodes[0];
        firstResult.click();
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('search-results').addEventListener('click', function (event) {
        if (event.target && event.target.classList.contains('stock-item')) {
            const symbol = event.target.dataset.symbol; 
            window.location.href = `/${symbol}/profile/`;
        }
    });
    document.querySelectorAll('.stock-symbol').forEach(function(element) {
        element.addEventListener('click', function () {
            const symbol = this.getAttribute('data-symbol'); 
            window.location.href = `/${symbol}/profile/`;
        });
    });
});
