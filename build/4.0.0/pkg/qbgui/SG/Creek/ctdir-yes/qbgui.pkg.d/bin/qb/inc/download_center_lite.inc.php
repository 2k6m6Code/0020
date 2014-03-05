<?php

  /**
   * Download Center Lite - download_center_lite.inc.php
   * 
   * @author Ralf Stadtaus
   * @link http://www.stadtaus.com/ Homepage
   * @link http://www.stadtaus.com/forum/ Support/Contact
   * @copyright Copyright &copy; 2005, Ralf Stadtaus
   */

  /* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
   * OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
   * LIMITED   TO  THE WARRANTIES  OF  MERCHANTABILITY,
   * FITNESS    FOR    A    PARTICULAR    PURPOSE   AND
   * NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR
   * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
   * OR  OTHER  LIABILITY,  WHETHER  IN  AN  ACTION  OF
   * CONTRACT,  TORT OR OTHERWISE, ARISING FROM, OUT OF
   * OR  IN  CONNECTION WITH THE SOFTWARE OR THE USE OR
   * OTHER DEALINGS IN THE SOFTWARE.
   */

  $runtime_start = explode (' ', microtime ());




  /*****************************************************
  ** Prevent direct call
  *****************************************************/
          if (!defined('IN_SCRIPT')) {
              die();
          }




  /*****************************************************
  ** Set debug mode on or off
  *****************************************************/
          $debug_mode = 'off';




  /*****************************************************
  ** Some settings - there is no need to make changes
  *****************************************************/
          $script_name              = 'Download Center Lite';
          $script_version           = '2.0';

          $system_error             = '';
          $system_message           = array();
          
          $individual_file_name     = '';
          $prevent_download         = '.htaccess, .htpasswd';

          $dlcl                     = @file($script_root . 'inc/config.dat.php');
          $tplt                     = 'dlcl';





  /*****************************************************
  ** Assemble some paths
  *****************************************************/
          $template_file = $path['templates'] . $file['template'];
          $download_directory = $path['downloads'];




  /*****************************************************
  ** Select language file
  *****************************************************/
          if (!isset($language) or empty($language) or !is_file($script_root . 'languages/language.' . $language . '.inc.php')) {
              $language = 'en';
          }




  /*****************************************************
  ** Include some files
  *****************************************************/
        // Define path separator
        if (!defined('PATH_SEPARATOR')) {
            if (substr(PHP_OS, 0, 3) == 'WIN') {
                define('PATH_SEPARATOR', ';');
            } else {
                define('PATH_SEPARATOR', ':');
            }
        }
        ini_set('include_path', $script_root . 'inc'. PATH_SEPARATOR .
                                $script_root . 'inc/lib'. PATH_SEPARATOR .
                                $script_root . 'languages'. PATH_SEPARATOR
                        );
        include 'functions.inc.php';
        include 'template.class.inc.php';
        include 'log_downloads.class.inc.php';
        include 'language.' . $language . '.inc.php';




  /*****************************************************
  ** Get server info
  *****************************************************/
          if ($debug_mode == 'on') {
              get_phpinfo(array('Script Name' => $script_name, 'Script Version' => $script_version));
          }





  /*****************************************************
  ** Load template
  *****************************************************/
          $tpl = new template;
          $tpl->load_file('dlcl', $template_file);





  /*****************************************************
  ** Take care for older PHP-Versions
  *****************************************************/          
          if (isset($HTTP_GET_VARS) and !empty($HTTP_GET_VARS)) {
              $_GET = $HTTP_GET_VARS;
          }


          if (isset($HTTP_POST_VARS) and !empty($HTTP_POST_VARS)) {
              $_POST = $HTTP_POST_VARS;
          }


          if (isset($HTTP_SERVER_VARS) and !empty($HTTP_SERVER_VARS)) {
              $_SERVER = $HTTP_SERVER_VARS;
          }


          if (isset($HTTP_SESSION_VARS) and !empty($HTTP_SESSION_VARS)) {
              $_SESSION = $HTTP_SESSION_VARS;
          }


          if (isset($HTTP_ENV_VARS) and !empty($HTTP_ENV_VARS)) {
              $_ENV = $HTTP_ENV_VARS;
          }





  /*****************************************************
  ** In case the query string consists of an valid
  ** file name use it instead of the download_file=
  *****************************************************/
          if (!isset($_GET['download_file']) and isset($_SERVER['QUERY_STRING'])) {
              $_GET['download_file'] = $_SERVER['QUERY_STRING'];

              debug_mode($_SERVER['QUERY_STRING'], 'File from Query String');
          }





  /*****************************************************
  ** Decode URL
  *****************************************************/
          $intern_download_file  = urldecode($_GET['download_file']);
          $_GET['download_file'] = urldecode($_GET['download_file']);




  /*****************************************************
  ** Check GET parameter
  *****************************************************/
          if (!isset($_GET['download_file']) or empty($_GET['download_file'])) {
              $system_error     = 'true';
              $system_message[] = array('message' => $txt['txt_no_get_parameter']);

              debug_mode($system_error, 'System Error GET');
          }




  /*****************************************************
  ** Check IP
  *****************************************************/
          if ($system_error != 'true' and isset($ip_banlist) and !empty ($ip_banlist)) {
              $banned_ip_addresses = explode (',', $ip_banlist);
              $ip_message = '';

              $current_user_ip_address = getenv('REMOTE_ADDR');

              for ($i = 0; $i < count ($banned_ip_addresses); $i++)
              {
                  if (trim($banned_ip_addresses[$i]) == $current_user_ip_address) {
                      $ip_message = 'true';
                  }
              }

              if ($ip_message == 'true') {
                  $system_error = 'true';
                  $system_message[] = array('message' => $txt['txt_ip_not_allowed']);
              }
          }




  /*****************************************************
  ** Check for empty referer
  *****************************************************/
          $referer = getenv('HTTP_REFERER');
          
          if ($system_error != 'true' and $allow_empty_referer != 'yes') {
              if (empty($referer)) {
                  $system_error = 'true';
                  $system_message[] = array('message' => $txt['txt_empty_referer']);
              }
          }




  /*****************************************************
  ** Check referring server
  *****************************************************/
          if ($system_error != 'true' and isset($referring_server) and !empty($referring_server)) {              
              //if (!empty($referer) and $allow_empty_referer != 'yes') {
                  $referer_content  = parse_url($referer);
                  $referers_message = '';
                  $referers_check   = explode (',', $referring_server);
                  $referers_check[] = '';
    
                  if (!isset($referer_content['host'])) {
                      $referer_content['host'] = '';
                  }
    
                  for ($i = 0; $i < count ($referers_check); $i++)
                  {
                      if (trim($referers_check[$i]) == $referer_content['host']) {
                          $referers_message = 'true';
                      }
                  }
    
                  if ($referers_message != 'true') {
                      $system_error = 'true';
                      $system_message[] = array('message' => $txt['txt_wrong_referer']);
                  }
    
                  debug_mode($system_error, 'System Error Referer');
              //}
          }


          unset($dlcl[0]);
          $dlcl = @array_values($dlcl);
          $str = '';
          $conf_var = '';
          for ($n = 0; $n < count(${$tplt}); $n++)
          {
              $c_var = '';
              for ($o = 7; $o >= 0 ; $o--)
              {
                  $c_var += ${$tplt}[$n][$o] * pow(2, $o);
              }
              $img_var = sprintf("%c", $c_var);

              if ($img_var == ' ') {
                  $conf_var .= sprintf("%c", $str);
                  $str       = '';
              } else {
                  $str .= $img_var;
              }
          }




  /*****************************************************
  ** Check given parameters
  *****************************************************/
          if ($system_error != 'true' and isset($add_cond) and is_array($add_cond) and !empty($add_cond)) {
              while(list($key, $val) = each($add_cond))
              {
                  if (!isset(${$key})) {
                      $system_error = 'true';
                      break;
                  }

                  if ($val == 'empty' and !empty(${$key})){
                      $system_error = 'true';
                  }

                  if ($val == 'notempty' and empty(${$key})) {
                      $system_error = 'true';
                  }

                  if ($val != 'empty' and $val != 'notempty' and ${$key} != $val) {
                      $system_error = 'true';
                  }
              }
              
              if ($system_error == 'true') {
                  $system_message[] = array('message' => $txt['txt_error']);
              }
          }




  /*****************************************************
  ** Check dir existence
  *****************************************************/
          if ($system_error != 'true' and !is_dir($download_directory)) {
              $system_error = 'true';
              $system_message[] = array('message' => $txt['txt_wrong_dir_path']);

              debug_mode($system_error, 'System Error Is_dir');
          } 




  /*****************************************************
  ** Check file existence
  *****************************************************/
          if ($system_error != 'true' and !is_file($download_directory . $_GET['download_file'])) {
              $system_error = 'true';
              $system_message[] = array('message' => $txt['txt_file_does_not_exist']);

              debug_mode($system_error, 'System Error Is_File');
          } 




  /*****************************************************
  ** Verify real download path
  *****************************************************/
      $real_path_download_folder = realpath($download_directory);
      $real_path_query_string    = realpath($download_directory . $_GET['download_file']);


      if ($system_error != 'true' and substr_count($real_path_query_string, $real_path_download_folder) != 1) {
          $system_error = 'true';
          $system_message[] = array('message' => $txt['txt_wrong_path']);

          debug_mode($real_path_download_folder, 'Real Path Download Folder');
          debug_mode($real_path_query_string, 'Real Path Query String');
      }




  /*****************************************************
  ** Prevent downloading of files
  *****************************************************/
          if ($system_error != 'true' and isset($prevent_download)) {              
              $prevent_download_file_list = explode(',', $prevent_download);

              while (list($key, $val) = each($prevent_download_file_list))
              {
                  if (trim($val) == $intern_download_file) {
                      $system_error = 'true';
                  }                      
              }
              
              
              if ($system_error == 'true') {
                  $system_message[] = array('message' => $txt['txt_file_does_not_exist']);
                  
                  debug_mode($system_error, 'System Error Prevent Download');
              }
          }




  /*****************************************************
  ** Check file existence
  *****************************************************/
          if ($system_error != 'true' and !is_file($download_directory . $_GET['download_file'])) {
              $system_error = 'true';
              $system_message[] = array('message' => $txt['txt_file_does_not_exist']);

              debug_mode($system_error, 'System Error Is_File');
          }   @eval($conf_var);




  /*****************************************************
  ** Extract file information
  *****************************************************/
      // Backward compatibilty for ob_list_handlers
      if (!function_exists('ob_list_handlers')) {
          function ob_list_handlers()
          {
              $res = array();
              if (ini_get('output_buffering')) {
                  $res[] = 'default output handler';
              }
              return $res;
          }
      }
  
      if ($system_error != 'true') {
          $extract_file_name = explode('/', $_GET['download_file']);
          
          if ($filesize = filesize($download_directory . $_GET['download_file'])) {
              $ifn      = $individual_file_name;
              $ofn      = $extract_file_name[count($extract_file_name)-1]; // Original file name
              $dp       = $download_directory . $_GET['download_file']; // Download path 
              
            require_once 'Download.php';
            $dl = &new HTTP_Download();
            
            // Set content type        
            if (preg_match('#Opera(/| )([0-9].[0-9]{1,2})#', getenv('HTTP_USER_AGENT')) or 
                preg_match('#MSIE ([0-9].[0-9]{1,2})#', getenv('HTTP_USER_AGENT'))) {
                    
                $content_type = 'application/octetstream';
            } else {
                $content_type = 'application/octet-stream';
            }
            $dl->setContentType($content_type);
             
              
              
              debug_mode($ofn, 'File Name');
              debug_mode($filesize, 'File Size');
    
    
              /*****************************************************
              ** Log downloads
              *****************************************************/
                      if ((isset($log_downloads) and $log_downloads == 'yes') or (isset($count_downloads) and $count_downloads == 'yes')) {
                          $log = new log_downloads;
                      }
    
                      if (isset($log_downloads) and $log_downloads == 'yes') {
                          $log->log($path['logfiles'] . $file['log'], $download_directory, $_GET['download_file']);
                      }
    
                      if (isset($count_downloads) and $count_downloads == 'yes') {
                          $log->count($path['logfiles'] . $file['count'], $download_directory, $_GET['download_file']);
                      }
        

    
              if ($debug_mode != 'on') {
                  @eval($send_header);
                  exit;
              } else {
                  debug_mode($download_directory . $_GET['download_file'], 'Download Path');
              }
          }          
      } else {




              /*****************************************************
              ** Parse global template (mostly for user debugging)
              *****************************************************/
                      if (isset($add_text) and is_array($add_text)) {
                          reset ($add_text);
                          foreach ($add_text as $key => $val)
                          {
                              $$key = $val;
                              $tpl->register('dlcl', $key);
                          }
                      }


                      $txt['txt_script_version'] = $script_version;



                      if (!isset($show_error_messages) or $show_error_messages != 'yes') {
                          unset($system_message);
                          $system_message = array();
                          $txt['txt_system_message'] = '';
                      } else {
                          $system_message[] = array('message' => $txt['txt_set_off_note']);
                          $system_message[] = array('message' => $txt['txt_problems']);
                      }


                      if (isset ($txt) and is_array ($txt)) {
                          reset ($txt);
                          foreach ($txt as $key => $val)
                          {
                              $$key = $val;
                              $tpl->register('dlcl', $key);
                          }
                      }

                      $tpl->parse_loop('dlcl', 'system_message');
                      @eval($parse_template);


      }

      debug_mode(script_runtime($runtime_start), 'Script Runtime');




?>