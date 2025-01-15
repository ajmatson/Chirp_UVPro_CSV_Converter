/**
 * Copyright 2025 Alan Matson
 *
 * Licensed under the MIT License.
 * See LICENSE.txt or https://opensource.org/licenses/MIT for details.
 */

/**
 * @author Alan Matson <alan(@)offgrid.technology>
 */
/**
 * @version [0.1a]
 */

<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['chirp_file'])) {
    $uploadDir = __DIR__ . '/uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);  // Create uploads directory if not exists
    }

    $uploadedFile = $uploadDir . basename($_FILES['chirp_file']['name']);
    if (move_uploaded_file($_FILES['chirp_file']['tmp_name'], $uploadedFile)) {
        // Run Python script
        $outputFileName = "Converted_UVPro.csv";
        $command = escapeshellcmd("python3 convert_chirp_uvpro.py \"$uploadedFile\" \"$outputFileName\"");
        exec($command, $output, $status);

        if ($status === 0) {
            // Download link
            echo "<h2>Conversion Successful!</h2>";
            echo "<a href='$outputFileName' download>Download UV-Pro CSV</a>";
        } else {
            echo "<p>Error: Could not run the Python script.</p>";
        }
    } else {
        echo "<p>File upload failed.</p>";
    }
} else {
    echo "<p>No file uploaded.</p>";
}
?>
