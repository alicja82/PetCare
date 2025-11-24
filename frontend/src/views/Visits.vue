<template>
  <div class="visits-container">
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Historia wizyt weterynaryjnych</h2>
        <button class="btn btn-primary" @click="showAddModal = true" :disabled="!hasPets">
          <i class="bi bi-plus-circle"></i> Dodaj wizytę
        </button>
      </div>

      <!-- No pets warning -->
      <div v-if="!hasPets" class="alert alert-warning">
        <i class="bi bi-exclamation-triangle"></i> Najpierw dodaj zwierzę, aby móc rejestrować wizyty weterynaryjne.
        <router-link to="/pets" class="alert-link ms-2">Przejdź do zwierząt</router-link>
      </div>

      <!-- Loading -->
      <div v-if="visitStore.loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Ładowanie...</span>
        </div>
      </div>

      <!-- Error -->
      <div v-if="visitStore.error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ visitStore.error }}
        <button type="button" class="btn-close" @click="visitStore.clearError()"></button>
      </div>

      <!-- Empty state -->
      <div v-if="!visitStore.loading && !visitStore.hasVisits && hasPets" class="text-center py-5">
        <i class="bi bi-hospital" style="font-size: 4rem; color: #ccc;"></i>
        <h4 class="mt-3">Brak wizyt weterynaryjnych</h4>
        <p class="text-muted">Dodaj pierwszą wizytę klikając przycisk powyżej</p>
      </div>

      <!-- Visits timeline -->
      <div v-if="visitStore.hasVisits" class="row">
        <div class="col-12">
          <div v-for="pet in petsWithVisits" :key="pet.id" class="mb-4">
            <div class="card shadow-sm">
              <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="bi bi-heart-fill"></i> {{ pet.name }}
                </h5>
                <button class="btn btn-sm btn-light" @click="openAddModalForPet(pet)">
                  <i class="bi bi-plus"></i> Dodaj wizytę
                </button>
              </div>
              <div class="card-body">
                <div class="timeline">
                  <div 
                    v-for="visit in getVisitsForPet(pet.id)" 
                    :key="visit.id" 
                    class="timeline-item mb-4"
                  >
                    <div class="timeline-marker"></div>
                    <div class="timeline-content card">
                      <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                          <div>
                            <h6 class="card-subtitle mb-2 text-muted">
                              <i class="bi bi-calendar3"></i> {{ formatDate(visit.visit_date) }}
                            </h6>
                            <h5 class="card-title mb-2">{{ visit.reason }}</h5>
                          </div>
                          <div class="btn-group">
                            <button class="btn btn-sm btn-warning" @click="editVisit(visit)">
                              <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" @click="confirmDelete(visit)">
                              <i class="bi bi-trash"></i>
                            </button>
                          </div>
                        </div>
                        
                        <div class="row">
                          <div class="col-md-6" v-if="visit.diagnosis">
                            <p class="mb-1"><strong>Diagnoza:</strong></p>
                            <p class="text-muted">{{ visit.diagnosis }}</p>
                          </div>
                          <div class="col-md-6" v-if="visit.treatment">
                            <p class="mb-1"><strong>Leczenie:</strong></p>
                            <p class="text-muted">{{ visit.treatment }}</p>
                          </div>
                        </div>

                        <div class="row mt-2">
                          <div class="col-md-6" v-if="visit.vet_name">
                            <p class="mb-1">
                              <i class="bi bi-person-badge"></i> 
                              <strong>Weterynarz:</strong> {{ visit.vet_name }}
                            </p>
                          </div>
                          <div class="col-md-6" v-if="visit.cost">
                            <p class="mb-1">
                              <i class="bi bi-cash"></i> 
                              <strong>Koszt:</strong> {{ visit.cost }} zł
                            </p>
                          </div>
                        </div>

                        <div v-if="visit.notes" class="mt-2">
                          <p class="mb-1"><strong>Notatki:</strong></p>
                          <p class="text-muted small">{{ visit.notes }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Visit Modal -->
    <VisitFormModal
      v-if="showAddModal || showEditModal"
      :visit="editingVisit"
      :pets="petStore.pets"
      :selectedPetId="selectedPetId"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useVisitStore } from '../stores/visit'
import { usePetStore } from '../stores/pet'
import VisitFormModal from '../components/VisitFormModal.vue'

const visitStore = useVisitStore()
const petStore = usePetStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const editingVisit = ref(null)
const selectedPetId = ref(null)

const hasPets = computed(() => petStore.hasPets)

const petsWithVisits = computed(() => {
  return petStore.pets.filter(pet => 
    visitStore.getVisitsByPetId(pet.id).length > 0
  )
})

onMounted(async () => {
  await petStore.fetchPets()
  
  // Load visits for all pets
  for (const pet of petStore.pets) {
    await visitStore.fetchVisitsByPet(pet.id)
  }
})

const getVisitsForPet = (petId) => {
  const visits = visitStore.getVisitsByPetId(petId)
  return visits.sort((a, b) => new Date(b.visit_date) - new Date(a.visit_date))
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('pl-PL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const openAddModalForPet = (pet) => {
  selectedPetId.value = pet.id
  showAddModal.value = true
}

const editVisit = (visit) => {
  editingVisit.value = visit
  selectedPetId.value = visit.pet_id
  showEditModal.value = true
}

const confirmDelete = async (visit) => {
  if (confirm(`Czy na pewno chcesz usunąć wizytę: ${visit.reason}?`)) {
    try {
      await visitStore.deleteVisit(visit.id)
    } catch (error) {
      // Error handled in store
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingVisit.value = null
  selectedPetId.value = null
}

const handleSave = async () => {
  // Reload visits
  for (const pet of petStore.pets) {
    await visitStore.fetchVisitsByPet(pet.id)
  }
  closeModal()
}
</script>

<style scoped>
.visits-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #dee2e6;
}

.timeline-item {
  position: relative;
}

.timeline-marker {
  position: absolute;
  left: -24px;
  top: 8px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #28a745;
  border: 3px solid white;
  box-shadow: 0 0 0 2px #dee2e6;
}

.timeline-content {
  margin-left: 20px;
  border-left: 3px solid #28a745;
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
}

.btn-warning {
  color: white;
}
</style>
