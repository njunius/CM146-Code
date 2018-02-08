# Nader Sleem nsleem
# Nick Junius njunius
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.has_resource = False

  def handle_event(self, message, details):

    if self.state is 'idle':
      # a small chance of deciding to steal from the slugs while idle
      if random.random() < 0.05:
        self.state = 'steal'
        self.body.set_alarm(1)
      
      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
		
    elif self.state == 'steal':
	  
      if message == 'timer':
        if self.has_resource == False:
		  steal_target = self.body.find_nearest('Nest')
        else:
		  steal_target = self.body.find_nearest('Resource')
        if steal_target:
          self.body.go_to(steal_target)
        self.body.set_alarm(1)
		  
      # once you have successfully stolen resources, return to idle
      if message == 'collide' and details['what'] == 'Nest':
	    if self.has_resource == False:
		  self.has_resource = True
		  
      elif message == 'collide' and details['what'] == 'Resource':
        if self.has_resource:
          target_resource = details['who']
          target_resource.amount += 0.25
          self.has_resource = False
          self.body.stop()
          self.state = 'idle'
          self.body.set_alarm(1)

      # still get curious when bumped by a slug
      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']
		  
    
class SlugBrain:

  def __init__(self, body):
	self.body = body
	self.state = 'listen'
	self.has_resource = False


  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  appropriate.)

	if message == 'order':
		if details == 'i':
			self.state = 'listen'
			self.body.stop()
		elif details == 'a':
			self.state = 'attack'
			self.body.set_alarm(random.random()+1)
		elif details == 'b':
			self.state = 'build'
			self.body.set_alarm(1)
		elif details == 'h':
			self.state = 'harvest'
			self.body.set_alarm(1)
		else:
			self.state = 'listen'
			self.body.go_to(details)
	
	elif message == 'timer':
		if self.body.amount < 0.5:
			self.state = 'flee'
			nearest_nest = self.body.find_nearest('Nest')
			if nearest_nest:
				self.body.go_to(nearest_nest)
		elif self.state == 'attack':
			try:
				enemy = self.body.find_nearest('Mantis')
				if enemy:
					self.body.follow(enemy)
			except ValueError:
				self.body.stop()

		elif self.state == 'build':
			nest = self.body.find_nearest('Nest')
			if nest:
				self.body.go_to(nest)
				
		elif self.state == 'harvest':
			if self.has_resource == False:
				harvest_target = self.body.find_nearest('Resource')
			else:
				harvest_target = self.body.find_nearest('Nest')
			if harvest_target: 
				self.body.go_to(harvest_target)
		self.body.set_alarm(1)
	elif message == 'collide':
		if details['what'] == 'Mantis' and self.state == 'attack':
			target = details['who']
			target.amount -= 0.05
		elif details['what'] == 'Nest':
			if self.state == 'build':
				target = details['who']
				target.amount += 0.01
			elif self.state == 'harvest':
				self.has_resource = False
			elif self.state == 'flee':
				self.body.amount = 1.0
				self.state = 'listen'
		elif details['what'] == 'Resource' and self.state == 'harvest':
			if self.has_resource == False:
				target = details['who']
				target.amount -= 0.25
				self.has_resource = True
	
	
	
	
        

world_specification = {
  'worldgen_seed': 11, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 2,
  'mantises': 8,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
