<?php
include('event_emitter.php'); 

class TestEmitter
{
	private $message;
	
	public function on()
	{ 
		 $message = "Test emitter is turned on";
	}       
}

/*
 * Testing EventEmitter functions
 */
class EventEmitterTest extends PHPunit_Framework_Testcase {
   
    // emitter on test
    public function testOn(){
        
        $mediator = new EventEmitter();
		
		$emitter = new TestEmitter();
        $emitter2 = new TestEmitter();

        $event_name = "emitter.on";
		$mediator->on($event_name, array($emitter, 'on'));

		$mediator->on($event_name, array($emitter2, 'on'));
		
		$this->assertEquals(1, count($mediator->events), "Number of events should be 1 but was %s." % count($mediator->events));
        $this->assertEquals(2, count($mediator->events[$event_name]), "Number of events with same name should be 2, but was %s." % count($mediator->events[$event_name]) );
    }
	
    //Remove listener test
	public function testRemove(){
        
        $mediator = new EventEmitter();
		
		$emitter = new TestEmitter();
        $emitter2 = new TestEmitter();
		
		$listener = array($emitter, 'on');
        $event_name = "emitter.on";
		$mediator->on($event_name, $listener);
		$listener2 = array($emitter2, 'on');
		$mediator->on($event_name, $listener2);
		
		$this->assertEquals(2, count($mediator->events[$event_name]), "Number of events with same name should be 2, but was %s." % count($mediator->events[$event_name]) );
        $mediator->removeListener($event_name, $listener);
		$this->assertEquals(1, count($mediator->events[$event_name]), "Number of events with same name should be 1, but was %s." % count($mediator->events[$event_name]) );
		$mediator->removeListener($event_name, $listener2);
		$this->assertTrue(0 == count($mediator->events));
	}
	
    // remove all listeners test
	public function testRemoveAll(){
		$mediator = new EventEmitter();
		
		$emitter = new TestEmitter();
        $emitter2 = new TestEmitter();
		
		$listener = array($emitter, 'on');
        $event_name = "emitter.on";
		$mediator->on($event_name, $listener);
		$listener2 = array($emitter2, 'on');
		$mediator->on("emitter2.on", $listener2);
		
		$mediator->on($event_name, $listener2);
		
		$this->assertEquals(2, count($mediator->events[$event_name]), $message = "Number of events with same name should be 2, but was %s." % count($mediator->events[$event_name]) );
        $mediator->removeAllListeners($event_name);
		$this->assertTrue(1 == count($mediator->events));
		
		$mediator->removeAllListeners();
		$this->assertTrue(0 == count($mediator->events));
		
	}
	
    // emit test
	public function testEmit(){
		$mediator = new EventEmitter();
		
		$emitter = new TestEmitter();
        $emitter2 = new TestEmitter();
		
		$listener = array($emitter, 'on');
        $event_name = "emitter.on";
		$mediator->on($event_name, $listener);
		
		$mediator->on($event_name, array($emitter2, 'on'));
		$mediator->emit($event_name);
		$this->assertTrue(TRUE);
	}
	
}
?>