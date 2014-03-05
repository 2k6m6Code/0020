<?PHP
//print_r($_POST['pkglocal']);//debug

function file_upload_error_message($error_code) {
    switch ($error_code) {
        case UPLOAD_ERR_INI_SIZE:
            return 'The uploaded file exceeds the upload_max_filesize directive in php.ini';
        case UPLOAD_ERR_FORM_SIZE:
            return 'The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form';
        case UPLOAD_ERR_PARTIAL:
            return 'The uploaded file was only partially uploaded';
        case UPLOAD_ERR_NO_FILE:
            return 'No target file was uploaded';
        case UPLOAD_ERR_NO_TMP_DIR:
            return 'Missing a temporary folder';
        case UPLOAD_ERR_CANT_WRITE:
            return 'Failed to write file to disk(not enough space)';
        case UPLOAD_ERR_EXTENSION:
            return 'File upload stopped by extension';
        default:
            return 'Unknown upload error';
    }
} 

if($_POST['pkglocal'] =="PKG1" || $_POST['pkglocal'] =="PKG2"){
echo $_POST['pkglocal'];
}else{
echo "<html><body>Error:Select Image1 or Image2</body></html>";
return 0;
}
$pkgdir =$_POST['pkglocal'];

if($_FILES['pkgfile']['error'] !=0){
echo "<html><body>Error:".file_upload_error_message($_FILES['pkgfile']['error'].'</body></html>');
return 0;
}
if(! stripos($_FILES['pkgfile']['name'], "pkg")){
echo "<html><body>Error:File type not PKG</body></html>";
return 0;
}

if (!is_dir("/tmp/$pkgdir")){
mkdir("/tmp/$pkgdir", 0777);
}

foreach(glob("/tmp/$pkgdir/*") as $file) {

unlink($file);
}

$uploaddir = "/tmp/".$pkgdir."/";
$uploadfile = $uploaddir . basename($_FILES['pkgfile']['name']);
move_uploaded_file($_FILES['pkgfile']['tmp_name'], $uploadfile);
// print_r($_FILES);
//phpinfo();
$outstr  =  "Select ".$_FILES['pkgfile']['name']." Upload [Done]";


//ob_start();
header('Content-Type: text/html; charset=utf-8');
echo '<html><body>';

echo $outstr;
echo '</body></html>';
//ob_end_flush();

?>