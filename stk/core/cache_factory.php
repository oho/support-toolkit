<?php
/**
 *
 * @package SupportToolkit
 * @copyright (c) 2012 phpBB Group
 * @license http://opensource.org/licenses/gpl-2.0.php GNU General Public License v2
 *
 */

/**
 * STK User class
 *
 * Suppor toolkit cache factory class
 */
class stk_core_cache_factory extends phpbb_cache_factory
{
	private $acm_type;

	public function __construct($acm_type)
	{
		$this->acm_type = $acm_type;
	}

	public function get_driver()
	{
		$class_name = 'stk_core_cache_driver_' . $this->acm_type;
		return new $class_name();
	}
}
