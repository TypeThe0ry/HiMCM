var filesApp = angular.module('FilesApp', ['ui.bootstrap']).config(function ($locationProvider) {
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false,
        rewriteLinks: false
    });
});

//controllers
filesApp.controller('FilesController', function ($scope, $http, $location, $sce, $timeout) {
    $scope.returnedFiles = [];
    $scope.Fiscal = 0;
    $scope.SchoolYearId = 0; //this is for searching collections of files from the drop down - not the modal
    $scope.LevelId = 0;
    $scope.FileNameId = 0;
    $scope.VersionId = 0;
    $scope.FileSchoolYearId = 0; //this is for searching individual files out of the modal - not the drop down
    $scope.Page = "1";
    $scope.IsFirstLoad = false;
    $scope.IsPaging = false;
    $scope.IsSearching = false;
    $scope.hrefLoc = location.href.replace('#' + location.href.split('#')[1], "");

    $scope.FiscalOptions = [
        { value: 0, name: "Choose Fiscal or Nonfiscal" },
        { value: 1, name: "Fiscal" },
        { value: 2, name: "Nonfiscal" }
    ];

    $scope.LevelOptions = [
        { value: 0, name: "Select a Level" },
        { value: 2, name: "State" },
        { value: 5, name: "District" },
        { value: 7, name: "School" }
    ];
    
    $scope.SchoolYearOptions = [];

    ////////// CLEAR SCOPE VARS  ////////////////////

    $scope.clearSelections = function () {
        $scope.SchoolYearId = 0;
        $scope.LevelId = 0;
        $scope.Fiscal = 0;
        $scope.FileNameId = 0;
        $scope.VersionId = 0;
        $scope.FileSchoolYearId = 0;
    }

    $scope.clearSelectionsAndRun = function () {
        $scope.clearSelections();
        $scope.searchDataChanging();
    }

    ////////// SET SCOPE VARS  ////////////////////

    $scope.setFiscal = function (fiscalId) {
        $scope.Fiscal = fiscalId;
    }

    $scope.setLevelId = function (levelId) {
        $scope.LevelId = levelId;
    }

    $scope.setSchoolYear = function (schoolYear) {
        $scope.SchoolYearId = schoolYear;
    }

    $scope.setFileNameId = function (fileNameId) {
        $scope.FileNameId = fileNameId;
    }

    $scope.setVersionId = function (versionId) {
        $scope.VersionId = versionId;
    }

    $scope.setFileSchoolYearId = function (fileSchoolYearId) {
        $scope.FileSchoolYearId = fileSchoolYearId;
    }

    $scope.setPage = function (page) {
        $scope.Page = page;
    };

    $(document).ready(function () {
        $scope.IsFirstLoad = true;
        $scope.loadDropdowns();
        $scope.getFileNameYearVersions();
        //check for hash in url
        if ($location.$$hash !== "") {
            $scope.updateSelectionsFromHash();
            $scope.generateSearchData();
            $scope.getFiles();
        }
    });

    $scope.runSearch = function () {
        $scope.generateSearchData();
        $scope.generateHash();
        //updating the hash will get the search result, no need to explicitly call it here
    };

    $scope.loadDropdowns = function () {        
        var url = $scope.hrefLoc.toLowerCase().replace("files.html", "").replace("files.asp", "datatables") + "/api/Lookup/";
        var schoolYearIndex;
        $http.get(url)
            .then(function successCallback(response) {

                $scope.SchoolYearOptions = response.data.schoolYears;

                for (let i = 0; i < $scope.SchoolYearOptions.length; i++) {
                    if ($scope.SchoolYearOptions[i].id.toString() === $scope.SchoolYearId.toString()) {
                        schoolYearIndex = i;
                        $scope.SchoolYearId = $scope.SchoolYearOptions[schoolYearIndex].id;
                    }
                }
            }, function errorCallback(error) {
                console.log("There is an error with the files HTTP request: " + "url");
            });
    }

    $scope.getFiles = function () {

        //maintain collection year selection - for some reason (possibly something with bootstrap?) it loses it before running this function.
        var levelIndex, fiscalIndex;

        for (let i = 0; i < $scope.FiscalOptions.length; i++) {
            if ($scope.FiscalOptions[i].value.toString() === $scope.Fiscal.toString()) {
                fiscalIndex = i;
                $scope.Fiscal = $scope.FiscalOptions[fiscalIndex].value;
            }
        }

        for (let i = 0; i < $scope.LevelOptions.length; i++) {
            if ($scope.LevelOptions[i].value.toString() === $scope.LevelId.toString()) {
                levelIndex = i;
                $scope.LevelId = $scope.LevelOptions[levelIndex].value;
            }
        }

        //get files
        $scope.IsSearching = true;

        $http.get($scope.hrefLoc.toLowerCase().replace("files.html", "").replace("files.asp", "datatables")
            + "/api/File/"
            + $scope.Fiscal + "/"
            + $scope.LevelId + "/"
            + $scope.SchoolYearId + "/"
            + $scope.FileNameId + "/"
            + $scope.VersionId + "/"
            + $scope.FileSchoolYearId)
            .then(function successCallback(response) {
                var schoolYearIndex;
                $scope.returnedSelectionGroups = response.data.selectionGroupModels;

                //maintain collection year selection - for some reason (possibly something with bootstrap?) it loses it before running this function.
                for (let i = 0; i < $scope.SchoolYearOptions.length; i++) {
                    if ($scope.SchoolYearOptions[i].id.toString() === $scope.SchoolYearId.toString()) {
                        schoolYearIndex = i;
                        $scope.SchoolYearId = $scope.SchoolYearOptions[schoolYearIndex].id;
                    }
                }

                $scope.totalItems = $scope.returnedSelectionGroups.length;
                $scope.itemsPerPage = 5;
                $scope.setPagedData();
                $scope.IsSearching = false;

            }, function errorCallback(error) {
                console.log("There is an error with the files HTTP request");
                $scope.IsSearching = false;
            });
    }

    $scope.getFileNameYearVersions = function () {

        $http.get($scope.hrefLoc.toLowerCase().replace("files.html", "").replace("files.asp", "datatables")
            + "/api/File")
            .then(function successCallback(response) {
                $scope.returnedFileNameYearVersions = response.data;

            }, function errorCallback(error) {
                console.log("There is an error with the FileNameYearVersions HTTP request");
            });
    }

    //format html content
    $scope.toTrustedHTML = function (htmlData) {
        return $sce.trustAsHtml(htmlData);
    }

    $scope.fileLinkClicked = function (fileNameId, versionId, fileSchoolYearId) {
        $('#yearModal').modal('hide'); 
        var id = Math.random();
        $scope.searchDataChangingId = id;

        $scope.FileNameId = fileNameId;
        $scope.VersionId = versionId;
        $scope.FileSchoolYearId = fileSchoolYearId;
        //if using file links in the modal, nullify existing dropdown selections
        $scope.SchoolYearId = 0;
        $scope.LevelId = 0;
        $scope.Fiscal = 0;

        $scope.Page = 1;

        $timeout(function () {
            if (id === $scope.searchDataChangingId) {
                $scope.runSearch();
            }
        }, 250);
    }

    $scope.searchDataChanging = function () {
        var id = Math.random();
        $scope.searchDataChangingId = id;
        //if using dropdowns, nullify existing selections of filename and version
        $scope.FileNameId = 0;
        $scope.VersionId = 0;
        $scope.FileSchoolYearId = 0;

        $scope.Page = 1;

        $timeout(function () {
            if (id === $scope.searchDataChangingId) {
                $scope.runSearch();
            }
        }, 250);
    }

    ////////////////GENERATE SEARCH DATA

    $scope.generateSearchData = function () {
        //create request data
        var fiscal, levelId, schoolYear, fileNameId, versionId, fileSchoolYearId, page;
        if ($scope.Fiscal > 0) fiscal = $scope.Fiscal;
        if ($scope.LevelId > 0) levelId = $scope.LevelId;
        if ($scope.SchoolYearId > 0) schoolYear = $scope.SchoolYearId;
        if ($scope.FileNameId > 0) fileNameId = $scope.FileNameId;
        if ($scope.VersionId > 0) versionId = $scope.VersionId;
        if ($scope.FileSchoolYearId > 0) fileSchoolYearId = $scope.FileSchoolYearId;

        if ($scope.Page !== "") page = $scope.Page;

        $scope.SearchData = {
            Fiscal: fiscal,
            LevelId: levelId,
            SchoolYearId: schoolYear,
            FileNameId: fileNameId,
            VersionId: versionId,
            FileSchoolYearId: fileSchoolYearId,
            Page: page
        };
    }

    //////////////////  HASH  ///////////////////////

    var hashChangeProcessing = false;

    window.onhashchange = function () {

        //prevent hash change from running twice
        if (hashChangeProcessing) return;
        hashChangeProcessing = true;
        setTimeout(function () { hashChangeProcessing = false; }, 250);
        if (!$scope.IsPaging) {
            //get results
            $scope.updateSelectionsFromHash();
            $scope.getFiles();
        }
    }

    $scope.generateHash = function () {

        ///$scope.SearchData is UNDEFINED except for page
        var hashData = angular.copy($scope.SearchData);

        var hashString = JSON.stringify(hashData).replace("{", "").replace("}", "");
        //remove quotes from json
        hashString = hashString.replace(/\"/g, "");

        var arrHash = hashString.split(',');
        for (var i = arrHash.length - 1; i >= 0; i--) {
            //remove nulls/empty string
            if (arrHash[i].split(':')[1] == "" || arrHash[i].split(':')[1] == "null") arrHash.splice(i, 1);
        }
        window.location.hash = "#" + arrHash.toString().replace(":00:00.000Z", "");
    }

    $scope.updateSelectionsFromHash = function () {
        var hasFiscal = false;
        var hasLevelId = false;
        var hasSchoolYear = false;
        var hasFileNameId = false;
        var hasVersionId = false;
        var hasFileSchoolYearId = false;
        // should always have page

        if ($location.$$hash != "") {
            var sHash = $location.$$hash;
            //test for /
            if (sHash.charAt(0) == "/") sHash = sHash.substring(1);
            //iterate through params
            var arrHash = sHash.split(',');
            for (var i = 0; i < arrHash.length; i++) {
                var oHash = arrHash[i].split(':');
                switch (oHash[0]) {
                    case "Fiscal": $scope.setFiscal(oHash[1]);
                        hasFiscal = true; break;
                    case "LevelId": $scope.setLevelId(oHash[1]);
                        hasLevelId = true; break;
                    case "SchoolYearId": $scope.setSchoolYear(oHash[1]);
                        hasSchoolYear = true; break;
                    case "FileNameId": $scope.setFileNameId(oHash[1]);
                        hasFileNameId = true; break;
                    case "VersionId": $scope.setVersionId(oHash[1]);
                        hasVersionId = true; break;
                    case "FileSchoolYearId": $scope.setFileSchoolYearId(oHash[1]);
                        hasFileSchoolYearId = true; break;
                    case "Page": $scope.setPage(oHash[1]); break;
                }
            }

            if (!hasFiscal) $scope.Fiscal = 0;
            if (!hasLevelId) $scope.LevelId = 0;
            if (!hasSchoolYear) $scope.SchoolYearId = 0;
            if (!hasFileNameId) $scope.FileNameId = 0;
            if (!hasVersionId) $scope.VersionId = 0;
            if (!hasFileSchoolYearId) $scope.FileSchoolYearId = 0;
        }
    }
    ////Paging
    $scope.setPagedData = function () {
        $scope.IsPaging = true;
        $scope.runSearch();

        var page = $scope.Page;

        if ($scope.totalItems > 0) {
            $scope.elementsGroupedBySelection = $scope.returnedSelectionGroups.slice((page - 1) * $scope.itemsPerPage, page * $scope.itemsPerPage);
        } else {
            $scope.elementsGroupedBySelection = [];
        }
        $scope.IsPaging = false;
    }
});