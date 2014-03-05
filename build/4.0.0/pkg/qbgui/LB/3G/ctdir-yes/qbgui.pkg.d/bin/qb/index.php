<?php

  /**
   * Download Center Lite - index.php
   * 
   * @author Ralf Stadtaus
   * @link http://www.stadtaus.com/ Homepage
   * @link http://www.stadtaus.com/forum/ Support/Contact
   * @copyright Copyright &copy; 2005, Ralf Stadtaus
   * @version 0.3
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




  /*****************************************************
  ** Script configuration - for a documentation of the
  ** following variables please take a look at the
  ** documentation file in the 'docu' directory.
  *****************************************************/

          $referring_server      = '';
          $allow_empty_referer   = 'yes';      /* (yes, no) */
          
          $ip_banlist            = '';         /* i.e: 127.0.0.1, 192.168.0.1, ... */

          $language              = 'en';       /* (en, de, it, sv, fr)  */

          $show_error_messages   = 'yes';      /* (yes, no) */


          $log_downloads         = 'no';       /* (yes, no) */
          $count_downloads       = 'no';       /* (yes, no) */


          $path['downloads']     = './downloads/';
          $path['templates']     = './templates/';
          $path['logfiles']      = './logfiles/';

          $file['template']      = 'index.tpl.html';
          $file['log']           = 'log.txt';
          $file['count']         = 'count.txt';




  /*****************************************************
  ** Add further words, text, variables and stuff
  ** that you want to appear in the template here.
  *****************************************************/
          $add_text = array(

                              'txt_additional' => 'Additional', //  {txt_additional}
                              'txt_more'       => 'More'        //  {txt_more}

                            );





  /*****************************************************
  ** Do not edit below this line - Ende der Einstellungen
  *****************************************************/









  

  
  
  
  /*****************************************************
  ** Send safety signal to included files
  *****************************************************/
          define('IN_SCRIPT', 'true');




  /*****************************************************
  ** Load script code
  *****************************************************/
          $script_root           = './';

          include($script_root . 'inc/download_center_lite.inc.php')




?>