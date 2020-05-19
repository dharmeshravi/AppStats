function initialize() { viewData(); }


setInterval(function() { viewData(); }, 60000);


function viewData() {
	var allcanvaz = document.getElementsByTagName("canvas");
	for (i=0; i<allcanvaz.length; i++) {
		visualizeData(allcanvaz[i].id);
	}
}


function visualizeData(application) {
	$.ajax({
		url: "/data/"+application,
		type: "GET",
		success: function(data) {
			var ctx = $("#"+application).get(0).getContext("2d");
			new Chart(ctx, {
				type: 'bar',
				data: data,
				options: {
					responsive: true,
					title:      {
						display: true,
						text: data.datasets[0].label,
						fontSize: 15,
						fontStyle: 'bold',
					},
					legend: {
						display: false
					},
					animation: { duration: 0 },
					scales: {
						xAxes: [{
							type: 'time',
							time: {
								unit: 'hour'
							},
							/* scaleLabel: {
								display:     true,
								labelString: 'DateTime'
							}, */
							ticks: {
								min: moment(data.minBound),
								max: moment(data.maxBound)
							}
						}],
						yAxes: [{
							scaleLabel: {
								display: true,
								beginAtZero: true,
								labelString: 'Status'
							},
							ticks: {
								min: 0,
								max: 1.5,
								stepSize: 1
							}
						}]
					},
					tooltips: {
						callbacks: {
							label: function(tooltipItem, data) {
								return data.datasets[0].message[tooltipItem.index];
							}
						}
					}
				}
			});
		}
	});
}
	