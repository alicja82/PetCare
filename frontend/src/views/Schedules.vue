<template>
  <div class="schedules-container">
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Harmonogram karmienia</h2>
        <button class="btn btn-primary" @click="showAddModal = true" :disabled="!hasPets">
          <i class="bi bi-plus-circle"></i> Dodaj harmonogram
        </button>
      </div>

      <!-- No pets warning -->
      <div v-if="!hasPets" class="alert alert-warning">
        <i class="bi bi-exclamation-triangle"></i> Najpierw dodaj zwierzę, aby móc tworzyć harmonogramy karmienia.
        <router-link to="/pets" class="alert-link ms-2">Przejdź do zwierząt</router-link>
      </div>

      <!-- Loading -->
      <div v-if="scheduleStore.loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Ładowanie...</span>
        </div>
      </div>

      <!-- Error -->
      <div v-if="scheduleStore.error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ scheduleStore.error }}
        <button type="button" class="btn-close" @click="scheduleStore.clearError()"></button>
      </div>

      <!-- Empty state -->
      <div v-if="!scheduleStore.loading && !scheduleStore.hasSchedules && hasPets" class="text-center py-5">
        <i class="bi bi-calendar-x" style="font-size: 4rem; color: #ccc;"></i>
        <h4 class="mt-3">Brak harmonogramów karmienia</h4>
        <p class="text-muted">Dodaj pierwszy harmonogram klikając przycisk powyżej</p>
      </div>

      <!-- Schedules by pet -->
      <div v-if="scheduleStore.hasSchedules">
        <div v-for="pet in petsWithSchedules" :key="pet.id" class="mb-4">
          <div class="card shadow-sm">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                <i class="bi bi-heart-fill"></i> {{ pet.name }}
              </h5>
              <button class="btn btn-sm btn-light" @click="openAddModalForPet(pet)">
                <i class="bi bi-plus"></i> Dodaj
              </button>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Godzina</th>
                      <th>Rodzaj karmy</th>
                      <th>Ilość</th>
                      <th>Częstotliwość</th>
                      <th>Notatki</th>
                      <th>Akcje</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="schedule in getSchedulesForPet(pet.id)" :key="schedule.id">
                      <td><strong>{{ schedule.feeding_time }}</strong></td>
                      <td>{{ schedule.food_type }}</td>
                      <td>{{ schedule.amount }}</td>
                      <td>
                        <span class="badge bg-info">{{ schedule.frequency || 'Codziennie' }}</span>
                      </td>
                      <td>{{ schedule.notes || '-' }}</td>
                      <td>
                        <button class="btn btn-sm btn-warning me-2" @click="editSchedule(schedule)">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" @click="confirmDelete(schedule)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Schedule Modal -->
    <ScheduleFormModal
      v-if="showAddModal || showEditModal"
      :schedule="editingSchedule"
      :pets="petStore.pets"
      :selectedPetId="selectedPetId"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useScheduleStore } from '../stores/schedule'
import { usePetStore } from '../stores/pet'
import ScheduleFormModal from '../components/ScheduleFormModal.vue'

const scheduleStore = useScheduleStore()
const petStore = usePetStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const editingSchedule = ref(null)
const selectedPetId = ref(null)

const hasPets = computed(() => petStore.hasPets)

const petsWithSchedules = computed(() => {
  return petStore.pets.filter(pet => 
    scheduleStore.getSchedulesByPetId(pet.id).length > 0
  )
})

onMounted(async () => {
  await petStore.fetchPets()
  
  // Load schedules for all pets
  for (const pet of petStore.pets) {
    await scheduleStore.fetchSchedulesByPet(pet.id)
  }
})

const getSchedulesForPet = (petId) => {
  return scheduleStore.getSchedulesByPetId(petId)
}

const openAddModalForPet = (pet) => {
  selectedPetId.value = pet.id
  showAddModal.value = true
}

const editSchedule = (schedule) => {
  editingSchedule.value = schedule
  selectedPetId.value = schedule.pet_id
  showEditModal.value = true
}

const confirmDelete = async (schedule) => {
  if (confirm(`Czy na pewno chcesz usunąć ten harmonogram karmienia?`)) {
    try {
      await scheduleStore.deleteSchedule(schedule.id)
    } catch (error) {
      // Error handled in store
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingSchedule.value = null
  selectedPetId.value = null
}

const handleSave = async () => {
  // Reload schedules
  for (const pet of petStore.pets) {
    await scheduleStore.fetchSchedulesByPet(pet.id)
  }
  closeModal()
}
</script>

<style scoped>
.schedules-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
}

.table {
  margin-bottom: 0;
}

.btn-warning {
  color: white;
}
</style>
