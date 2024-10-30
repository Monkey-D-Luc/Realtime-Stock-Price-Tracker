
const timestamps = JSON.parse(document.getElementById('data-timestamps').textContent);
const closePrices = JSON.parse(document.getElementById('data-close-prices').textContent);

const ctx = document.getElementById('stockChart').getContext('2d');
const stockChart = new Chart(ctx, {
    type: 'line',  
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Giá đóng cửa',
            data: closePrices,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false,
            borderWidth: 1
        }]
    },
    options: {
        responsive: true, 
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Thời gian'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Giá đóng cửa (USD)'
                },
                beginAtZero: false
            }
        }
    }
});
