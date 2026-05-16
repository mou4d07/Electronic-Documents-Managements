document.addEventListener('DOMContentLoaded', function () {
    var viewerElement = document.getElementById('openseadragon-viewer');
    var overlay = document.getElementById('loading-overlay');
    if (viewerElement) {
                    var viewer = OpenSeadragon({
                        id: "openseadragon-viewer",
                        //prefixUrl: window.appBasePath + "lib/openseadragon-bin-4.1.1/images/",
                        prefixUrl: "/ged/lib/openseadragon-bin-4.1.1/images/",
                        tileSources: viewerElement.getAttribute('data-dzi-path'),
                        showNavigator: true,
                        showRotationControl: true
                    });
        viewer.addHandler('open', function () {
            if (overlay) overlay.style.display = 'none';

            // Create the print button element with custom background images
            var printButtonElement = document.createElement('div');
            printButtonElement.id = 'print-button';
            printButtonElement.className = 'print-button-osd';

                        // Create the OpenSeadragon button
                        var printButton = new OpenSeadragon.Button({
                            tooltip: 'Print',
                            onRelease: function() {
                                printOpenSeadragonView(viewer);
                            },
                            srcRest: null, 
                            srcGroup: null,
                            srcHover: null,
                            srcActive: null,
                            element: printButtonElement 
                        });
                        viewer.addControl(printButton.element, { anchor: OpenSeadragon.ControlAnchor.BOTTOM_RIGHT });
                        // Append the print button element directly to the viewer's element
                        //viewer.element.appendChild(printButton.element);
                    });
            
        function printOpenSeadragonView(viewer) {
            if (viewer && viewer.drawer && viewer.drawer.canvas) {
                var imgData = viewer.drawer.canvas.toDataURL("image/png");
                var printWindow;
            
                try {
                    printWindow = window.open('', '_blank');
                    if (!printWindow) {
                        throw new Error("Le bloqueur de fenêtres publicitaires a empêché l'ouverture de la fenêtre d'impression. Veuillez l'autoriser pour ce site.");
                    }
            
                    printWindow.document.write('<html><head><title>Print</title><style>html, body { margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; } img { width: 100%; height: 100%; object-fit: cover; }</style></head><body>');
                    var img = printWindow.document.createElement("img");
                    img.src = imgData;
                    printWindow.document.body.appendChild(img);
                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    printWindow.focus();
            
                    // Use a timeout to ensure the image has time to load before printing
                    setTimeout(function() {
                        printWindow.print();
                        printWindow.close();
                    }, 500);
            
                } catch (e) {
                    alert(e.message);
                    console.error(e);
                }
            } else {
                console.warn("OpenSeadragon viewer or canvas not ready for printing.");
            }
        }
    }

    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle');

    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        const icon = toggleBtn.querySelector('i');
        icon.classList.toggle('fa-chevron-left');
        icon.classList.toggle('fa-chevron-right');
    });
});
