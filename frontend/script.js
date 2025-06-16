fetch("http://localhost:8020/csv")
  .then(res => res.text())
  .then(csv => {
    const rows = csv.trim().split("\n").map(row => row.split(","));
    const times = rows.map(row => row[0]);
    const giaVang = rows.map(row => parseInt(row[1].replace(/,/g, "")));

    new Chart(document.getElementById("chart"), {
      type: 'line',
      data: {
        labels: times,
        datasets: [{
          label: 'Giá Nhẫn tròn 999 (mua)',
          data: giaVang,
          borderColor: 'gold',
          tension: 0.3,
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            ticks: { maxRotation: 90, minRotation: 45 }
          },
          y: {
            beginAtZero: false
          }
        }
      }
    });
  });
