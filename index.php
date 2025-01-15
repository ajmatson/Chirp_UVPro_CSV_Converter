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

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CHIRP to UV-Pro Converter</title>
</head>
<body>
    <h1>Upload CHIRP Export File</h1>
    <P>Last Updated: 15 January 2025</p>
    <p>This tool is in extreme ALPHA, use at your own risk! Feedback is welcomed, feel free to email me at alan(@)offgrid.technology<br />This tool takes the exported .csv file from CHIRP and converts it to the UV-Pro format.<br />
Since the UV-Pro cannot take more than 30 channels ensure your export is 30 channels or less. I am working on a way to split into banks but that will take some time.</p>
    <form action="process_upload.php" method="post" enctype="multipart/form-data">
        Select CSV file to upload:
        <input type="file" name="chirp_file" accept=".csv">
        <input type="submit" value="Upload and Convert">
    </form>
<br /><br />
<p><b>Note:</b><br />
There is a known issue where after converting the file if you convert a subsequent one it gives you the cached<br />
output from the originally converted on. To temporarily get around this you can run this in private/incognito <br />
browser mode. We will update when fixed.</p>
<p>We are aware that there was a mixup in the TX and RX Frequencies, we adjusted the script and it worked in testing. <br />
If it is still broken please let us know on our Instagram or Facebook Pages. They are listed at https://www.offgrid.technology</p>
</body>
</html>
