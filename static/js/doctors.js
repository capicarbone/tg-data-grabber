
function DoctorsCtrl($scope, $window){

	$window.init= function(){
		$scope.$apply($scope.load_endpoints);
	};

	$scope.load_endpoints = function(){

		var host = window.location.host;
		var ROOT = '//' + host + '/_ah/api';

		gapi.client.load('doctors', 'v1', function() {
			$scope.is_backend_ready = true;
			$scope.show_doctors();

		}, ROOT);
	};

	$scope.show_doctors = function(){
		gapi.client.doctors.all().execute(function(resp){
			$scope.doctors = resp.doctors;
			$scope.$apply();
		});
	};

	$scope.send_email = function(r){
		$window.alert(r);
	};

	$scope.doctors = [];
}


function init_endpoints(){
	window.init();
}
