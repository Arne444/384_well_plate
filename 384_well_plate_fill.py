## Fill 384 well plate 

from opentrons import robot, instruments, containers

##Protocol: 
	# Add water to 384 plate
	# Add reagent 1 to 384 plate
	# Add reagent 2 to 384 plate
	# carry out _ replicates of reaction
	
#define containers
output = containers.load('384-plate', 'B2', 'output')
trash = containers.load('trash-box', 'A3')
p200rack = containers.load('tiprack-200ul', 'A1', 'p200_rack')

#Create 6x12 p20 tip rack container
containers.create(
	'tiprack-200ul-6x12',
	grid=(6,12),
	spacing=(9, 9),
	diameter=5,
	depth=60
)

p20rack = containers.load('tiprack-200ul-6x12', 'B2', 'p20_rack')

#Create 3x6 2ml tube rack for DNA samples
containers.create(
	'3x6-tube-rack-2ml',
	grid=(3,6),
	spacing=(19.5,19.5),
	diameter=9.5,
	depth=40
)

source_tubes = containers.load('3x6-tube-rack-2ml', 'C3', 'source_rack')

#define pipettes
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
reagent_1_volumes = [5, 5, 7]
reagent_2_volume = 2
water_volumes = []
for v in reagent_1_volumes:
	water_volumes.append(total_volume - v - reagent_2_volume)

replicates = 16
num_reagent_1 = len(reagent_1_volumes)
total_all = num_reagent_1 * replicates

reagent_1_replicates = []
for i in reagent_1_volumes:
	reagent_1_replicates.append(i * replicates)

#define source locations
water_source = source_tubes.wells('A1')
reagent_2_source = source_tubes.wells('C1')
reagent_1_sources = source_tubes.wells('A2', to= 'C2')

#distribute water
p200.distribute(
	water_volumes,
	water_source,
	output.wells('A1', length=total_all),
	blow_out=True,
	touch_tip=True
)

#distribute reagent_1
p20.transfer(
	reagent_1_volumes,
	reagent_1_sources,
	output.wells('A1', length=reagent_1_replicates),
	mix_after=(3, 7),
	blow_out=True,
	touch_tip=True
)

#distribute reagent_2
p20.transfer(
	reagent_2_volume,
	reagent_2_source,
	output.wells('A1', length=total_all),
	mix_after=(3, 4),
	blow_out=True,
	touch_tip=True
)

#mix
p200.pick_up_tip()
p200.mix('A1', length=total_all),
p200.drop_tip()
	
