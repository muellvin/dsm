// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Create a Paper.js project
    paper.setup('paperCanvas');

    // Define variables for storing points and paths
    var points = [];
    var paths = [];

    // Create a layer to hold the paths
    var pathLayer = new paper.Layer();

    // Event handler for mouse click on canvas
    function onMouseDown(event) {
        // Create a new point at the mouse position
        var point = new paper.Point(event.offsetX, event.offsetY);
        console.log(point);
        points.push(point);

        // Create a circle symbol to represent the point
        var circle = new paper.Path.Circle({
            center: point,
            radius: 2,
            fillColor: 'black'
        });

        // Create a path connecting all points
        var path = new paper.Path({
            segments: points,
            strokeColor: 'black'
        });
        paths.push(path);

        // Add the circle to the pathLayer
        pathLayer.addChild(circle);

        // Refresh the view to show the updated paths
        paper.view.draw();
    }

    // Attach the event handler to the canvas
    var canvas = document.getElementById('paperCanvas');
    canvas.addEventListener('mousedown', onMouseDown);
});

