<?php

  /**
   * Download Center Lite - index.php
   * 
   * @author Ralf Stadtaus
   * @link http://www.stadtaus.com/ Homepage
   * @link http://www.stadtaus.com/forum/ Support/Contact
   * @copyright Copyright &copy; 2005, Ralf Stadtaus
   * @version 1.2
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
  ** List of  some example extenstions
  *****************************************************/
          $extension_list = array('bmp', 'dat', 'doc', 'gif', 'html', 'jpg', 'mdb', 'pdf', 'php', 'png', 'ppt', 'rar', 'rtf', 'tar', 'tif', 'txt', 'xls', 'zip', 'tar.gz');




  /*****************************************************
  ** Include template class
  *****************************************************/
          include('./inc/template.class.inc.php');





  /*****************************************************
  ** Load template
  *****************************************************/
          $tpl = new template;
          $tpl->load_file('global', './templates/test.tpl.html');




  /*****************************************************
  ** Parse global template (mostly for user debugging)
  *****************************************************/
          if (isset($add_text) and is_array($add_text)) {
              reset ($add_text);
              foreach ($add_text as $key => $val)
              {
                  $$key = $val;
                  $tpl->register('global', $key);
              }
          }


          if (isset($extension_list) and !empty($extension_list) and is_array($extension_list)) {
              for($i = 0;  $i < count($extension_list); $i++)
              {
                  $extensions[] = array('EXT' => strtoupper($extension_list[$i]), 'ext' => strtolower($extension_list[$i]));
              }
          }


          $tpl->parse_loop('global', 'system_message');
          $tpl->parse_loop('global', 'extensions');

          if (isset ($txt) and is_array ($txt)) {
              reset ($txt);
              foreach ($txt as $key => $val)
              {
                  $$key = $val;
                  $tpl->register('global', $key);
              }
          }

          $tpl->parse('global');
          $tpl->print_file('global');