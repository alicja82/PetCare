<template>
  <div class="pets-container">
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Moje zwierzęta</h2>
        <button class="btn btn-primary" @click="showAddModal = true">
          <i class="bi bi-plus-circle"></i> Dodaj zwierzę
        </button>
      </div>

      <!-- Loading -->
      <div v-if="petStore.loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Ładowanie...</span>
        </div>
      </div>

      <!-- Error -->
      <div v-if="petStore.error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ petStore.error }}
        <button type="button" class="btn-close" @click="petStore.clearError()"></button>
      </div>

      <!-- Empty state -->
      <div v-if="!petStore.loading && !petStore.hasPets" class="text-center py-5">
        <i class="bi bi-inbox" style="font-size: 4rem; color: #ccc;"></i>
        <h4 class="mt-3">Nie masz jeszcze żadnych zwierząt</h4>
        <p class="text-muted">Dodaj swojego pierwszego pupila klikając przycisk powyżej</p>
      </div>

      <!-- Pets grid -->
      <div v-if="petStore.hasPets" class="row g-4">
        <div v-for="pet in petStore.pets" :key="pet.id" class="col-12 col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm pet-card">
            <div class="pet-image-container">
              <img 
                :src="getPetImage(pet)" 
                class="card-img-top" 
                :alt="pet.name"
                @error="handleImageError"
              />
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ pet.name }}</h5>
              <p class="text-muted mb-2">
                <i class="bi bi-tag"></i> {{ pet.species }} 
                <span v-if="pet.breed">• {{ pet.breed }}</span>
              </p>
              <div class="pet-info">
                <span v-if="pet.age" class="badge bg-info me-2">{{ pet.age }} lat</span>
                <span v-if="pet.weight" class="badge bg-secondary">{{ pet.weight }} kg</span>
              </div>
              <div v-if="pet.tags && pet.tags.length" class="mt-2">
                <span v-for="tag in pet.tags" :key="tag" class="badge bg-light text-dark me-1">
                  {{ tag }}
                </span>
              </div>
            </div>
            <div class="card-footer bg-transparent">
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-primary flex-fill" @click="viewPet(pet)">
                  <i class="bi bi-eye"></i> Szczegóły
                </button>
                <button class="btn btn-sm btn-outline-secondary" @click="editPet(pet)">
                  <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(pet)">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <PetFormModal 
      :show="showAddModal || showEditModal"
      :pet="editingPet"
      @close="closeModal"
      @save="handleSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePetStore } from '../stores/pet'
import { useRouter } from 'vue-router'
import PetFormModal from '../components/PetFormModal.vue'

const petStore = usePetStore()
const router = useRouter()

const showAddModal = ref(false)
const showEditModal = ref(false)
const editingPet = ref(null)

onMounted(() => {
  petStore.fetchPets()
})

const getPetImage = (pet) => {
  if (pet.photo_url) {
    return `http://127.0.0.1:5000${pet.photo_url}`
  }
  return 'https://via.placeholder.com/300x200?text=No+Photo'
}

const handleImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/300x200?text=No+Photo'
}

const viewPet = (pet) => {
  router.push(`/pets/${pet.id}`)
}

const editPet = (pet) => {
  editingPet.value = pet
  showEditModal.value = true
}

const confirmDelete = async (pet) => {
  if (confirm(`Czy na pewno chcesz usunąć ${pet.name}?`)) {
    try {
      await petStore.deletePet(pet.id)
    } catch (error) {
      // Error is handled in store
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingPet.value = null
}

const handleSave = async () => {
  await petStore.fetchPets()
  closeModal()
}
</script>

<style scoped>
.pets-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.pet-card {
  transition: transform 0.2s;
}

.pet-card:hover {
  transform: translateY(-5px);
}

.pet-image-container {
  height: 200px;
  overflow: hidden;
  background-color: #f8f9fa;
}

.pet-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pet-info {
  margin-top: 10px;
}
</style>
