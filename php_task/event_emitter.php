<?php

interface EventEmitterInterface
{
	public function on($event, callable $listener);
	public function removeListener($event, callable $listener);
	public function removeAllListeners($event = null);
	public function emit($event, array $attr=null);
}

class EventEmitter implements EventEmitterInterface
{
	public $events = array();

	public function on($event, callable $listener1)
	{
		if (!array_key_exists($event, $this->events))
		{
			$this->events[$event] = array();
		}

		array_push($this->events[$event], $listener1);
	}

	public function removeListener($event, callable $listener)
	{
		if (array_key_exists($event, $this->events))
		{
			$index = array_search($listener, $this->events[$event]);
			
			if ( $index !== false ) {
				unset($this->events[$event][$index] );
			}
			
			if(count($this->events[$event])==0) 
			{
				unset($this->events[$event]);
			}
		}
	}

	public function removeAllListeners($event = null)
	{
		if ($event == null)
		{
			$this->events = array();
		}
		else if (array_key_exists($event, $this->events))
		{
			unset($this->events[$event] );
		}
	}
	 
	public function emit($event, array $attr=null)
	{
		if (array_key_exists($event, $this->events))
		{
			foreach($this->events[$event] as $item)
			{		
				if(!empty($attr))
				{
					call_user_func_array($item, $attr);
				}
				else
				{
					call_user_func($item);
				}
			}
		}
	}
}
?>