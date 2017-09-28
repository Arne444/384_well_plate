## Perform 2-component reaction in 384-plate with variable "reagent 1" and replicates.

from opentrons import robot, instruments, containers

##Protocol: 
	# Add water to 384 plate
	# Add reagent 1 to 384 plate
	# Add reagent 2 to 384 plate
	# carry out _ replicates of reaction
	
	## input required volumes in ###INPUT###
	
##Define containers
output = containers.load('384-plate', 'C2', 'output')
trash = containers.load('trash-box', 'A3')
p200rack = containers.load('tiprack-200ul', 'A1', 'p200_rack')
trough = containers.load('trough-12row', 'A2', 'trough')

#Create 6x12 p20 tip rack container
containers.create(
	'tiprack-200ul-6x12',
	grid=(6,12),
	spacing=(9, 9),
	diameter=5,
	depth=60
)

p20rack = containers.load('tiprack-200ul-6x12', 'E1', 'p20_rack')

#Create 3x6 2ml tube rack for DNA samples
containers.create(
	'3x6-tube-rack-2ml',
	grid=(3,6),
	spacing=(19.5,19.5),
	diameter=9.5,
	depth=40
)

reagent_1_tubes = containers.load('3x6-tube-rack-2ml', 'C3', 'reagent_1_tubes')
reagent_2_tubes = containers.load('3x6-tube-rack-2ml', 'C1', 'reagent_2_tubes')

##Define pipettes
p20 = instruments.Pipette(
	tip_racks=[p20rack],
	trash_container=trash,
	min_volume=2,
	max_volume=20,
	axis="a"
)

p200 = instruments.Pipette(
	tip_racks=[p200rack],
	trash_container=trash,
	min_volume=20,
	max_volume=200,
	axis="b"
)

###INPUT### volumes for reaction
total_volume = 50
reagent_1_volumes = [5, 5, 6, 7, 7, 10]
reagent_2_volume = 2
water_volumes = []
for v in reagent_1_volumes:
	water_volumes.append(total_volume - v - reagent_2_volume)

replicates = 3
total_all = num_reagent_1 * replicates

#define source locations
water_source = trough.wells('A1')
reagent_2_source = reagent_2_tubes.wells('A1')

##Commands

#distribute water
for i in range(len(water_volumes)):
	p200.distribute(
		water_volumes[i], water_source, output.wells(i*16, length=(replicates), skip=8), 
		touch_tip=True)

#distribute reagent_1
for i in range(len(reagent_1_volumes)):
	p20.distribute(
		reagent_1_volumes[i], reagent_1_tubes(i), output.wells(i*16, length=(replicates), skip=8),
		touch_tip=True)
	
#distribute reagent_2
p20.transfer(
	reagent_2_volume,
	reagent_2_source,
	output.wells('A1', length=total_all),
	mix_after=(3, 4),
	blow_out=True,
	touch_tip=True,
	new_tip='always'
)

#mix
for i in range(total_all):
	p200.pick_up_tip()
	p200.mix(3, 48),
	blow_out=True,
	touch_tip=True,
	p200.drop_tip()
