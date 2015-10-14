# Unit 30 mins
MAX_HOURS = 10
MAX_SHIFT_HOURS = 7

class TimeSlot:
  def __init__(self, id):
    self.id = id
    self.available_workers = []
    self.number_of_workers = 0
    self.worker = None
    self.slot_before = None
    self.slot_after = None

  def __repr__(self):
    return "TimeSlot(" + self.id + "," + str(self.number_of_workers) +")"

  def add_worker(self, worker):
    self.available_workers.append(worker)
    self.number_of_workers += 1

  # Should be used after available_workers list is sorted
  def get_worker(self):
    if self.available_workers:
      return self.available_workers.pop(0)

  def assign_worker(self, worker):
    self.worker = worker
    worker.hours += 1

  # Sort available workers in terms of decreasing order
  def sort(self):
    self.available_workers.sort(key=lambda x: x.preference[self.id], reverse=True)


class Worker:
  def __init__(self,id):
    self.id = id
    self.hours = 0
    self.preference = {}

  def __repr__(self):
    return "Worker(" + self.id + "," + str(self.hours) + ")"

  def update_pref(self, time_slot_id, pref):
    self.preference[time_slot_id] = pref

  def get_pref(self, time_slot_id):
    return self.preference[time_slot_id]

  def can_work(self):
    return self.hours < MAX_HOURS

### other functions
def dict_val_to_list(dictionary):
  result = []
  for key in dictionary:
    result.append(dictionary[key])
  return result

# timeslots is a dictionary that has id as key and timeslot and val
def sort_all_time_slots(time_slots):
  for key in time_slots:
    time_slots[key].sort()

def assign_adj_time_slots(time_slot, worker):
  count = 1
  slot_before = time_slot.slot_before
  slot_after = time_slot.slot_after
  while count < MAX_SHIFT_HOURS and worker.can_work(): # max duration of shift
    pref_before, pref_after = 0, 0
    if slot_before:
      if not slot_before.worker:
        pref_before = worker.get_pref(slot_before.id)
    if slot_after:
      if not slot_after.worker:
        pref_after = worker.get_pref(slot_after.id)

    if pref_before or pref_after:
      if pref_before >= pref_after:
        slot_before.assign_worker(worker)
        slot_before = slot_before.slot_before
      else:
        slot_after.assign_worker(worker)
        slot_after = slot_after.slot_after
      count += 1
    else:
      return

def print_result(time_slot_list, workers):
  print "RESULT"
  time_slot_list.sort(key=lambda x: x.id)
  for time_slot in time_slot_list:
    print  time_slot.id + " " + str(time_slot.worker)

  print "===="
  for key in workers:
    worker = workers[key]
    print  worker.id + " - Hours: " + str(worker.hours)