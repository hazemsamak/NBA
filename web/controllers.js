// CONTROLLERS
weatherApp.controller("homeController", [
  "$scope",
  "$location",
  "$window",
  "$resource",
  "$http",
  function($scope, $location, $window, $resource, $http) {
    //    $http.get('movies.json').success(function (data){
    //        console.log('Data '+data);
    //        $scope.movies = data;
    //	});

    $scope.loading = true;
//    $http
//      .get("https://e2nrf7dpzl.execute-api.us-east-1.amazonaws.com/live")
//      .success(function(data) {
//        console.log("Data " + data);
//        $scope.movies = data;
//        $scope.loading = false;
//      });
    $http.get("matches.json")
            .success(function (data) {
                console.log("Data " + data);
                $scope.matches = data;
                $scope.loading = false;
            })
            .error(function (data) {
                console.log("there was an error");
            });
  }
]);
