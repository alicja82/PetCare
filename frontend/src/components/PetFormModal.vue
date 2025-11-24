<template>
  <div class="modal fade" :class="{ show: show }" :style="{ display: show ? 'block' : 'none' }" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ pet ? 'Edytuj zwierzę' : 'Dodaj nowe zwierzę' }}</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="save">
            <div class="row">
              <!-- Name -->
              <div class="col-md-6 mb-3">
                <label for="name" class="form-label">Imię *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="name" 
                  v-model="formData.name" 
                  required
                />
              </div>

              <!-- Species -->
              <div class="col-md-6 mb-3">
                <label for="species" class="form-label">Gatunek *</label>
                <select class="form-select" id="species" v-model="formData.species" required>
                  <option value="">Wybierz...</option>
                  <option value="Pies">Pies</option>
                  <option value="Kot">Kot</option>
                  <option value="Królik">Królik</option>
                  <option value="Ptak">Ptak</option>
                  <option value="Inne">Inne</option>
                </select>
              </div>

              <!-- Breed -->
              <div class="col-md-6 mb-3">
                <label for="breed" class="form-label">Rasa</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="breed" 
                  v-model="formData.breed"
                />
              </div>

              <!-- Age -->
              <div class="col-md-6 mb-3">
                <label for="age" class="form-label">Wiek (lata)</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="age" 
                  v-model.number="formData.age"
                  min="0"
                  max="50"
                />
              </div>

              <!-- Weight -->
              <div class="col-md-6 mb-3">
                <label for="weight" class="form-label">Waga (kg)</label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="weight" 
                  v-model.number="formData.weight"
                  min="0"
                  step="0.1"
                />
              </div>

              <!-- Photo -->
              <div class="col-md-6 mb-3">
                <label for="photo" class="form-label">Zdjęcie</label>
                <input 
                  type="file" 
                  class="form-control" 
                  id="photo" 
                  @change="handleFileChange"
                  accept="image/*"
                />
                <div v-if="photoPreview" class="mt-2">
                  <img :src="photoPreview" alt="Preview" style="max-width: 200px; max-height: 200px;" />
                </div>
              </div>

              <!-- Tags -->
              <div class="col-12 mb-3">
                <label for="tags" class="form-label">Tagi (oddziel przecinkami)</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="tags" 
                  v-model="tagsInput"
                  placeholder="np. przyjazny, energiczny, lubi dzieci"
                />
              </div>

              <!-- Notes -->
              <div class="col-12 mb-3">
                <label for="notes" class="form-label">Notatki</label>
                <textarea 
                  class="form-control" 
                  id="notes" 
                  v-model="formData.notes"
                  rows="3"
                ></textarea>
              </div>
            </div>

            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="close">Anuluj</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ pet ? 'Zapisz zmiany' : 'Dodaj zwierzę' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div v-if="show" class="modal-backdrop fade show"></div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { usePetStore } from '../stores/pet'

const props = defineProps({
  show: Boolean,
  pet: Object
})

const emit = defineEmits(['close', 'save'])

const petStore = usePetStore()
const formData = ref({
  name: '',
  species: '',
  breed: '',
  age: null,
  weight: null,
  photo: null,
  tags: [],
  notes: ''
})

const tagsInput = ref('')
const photoPreview = ref(null)
const loading = ref(false)
const error = ref(null)

watch(() => props.pet, (newPet) => {
  if (newPet) {
    formData.value = {
      name: newPet.name || '',
      species: newPet.species || '',
      breed: newPet.breed || '',
      age: newPet.age || null,
      weight: newPet.weight || null,
      photo: null,
      tags: newPet.tags || [],
      notes: newPet.notes || ''
    }
    tagsInput.value = newPet.tags ? newPet.tags.join(', ') : ''
    
    if (newPet.photo_url) {
      photoPreview.value = `http://127.0.0.1:5000${newPet.photo_url}`
    }
  } else {
    resetForm()
  }
}, { immediate: true })

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.photo = file
    const reader = new FileReader()
    reader.onload = (e) => {
      photoPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const save = async () => {
  loading.value = true
  error.value = null

  try {
    // Parse tags
    const tags = tagsInput.value
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0)
    
    formData.value.tags = tags

    if (props.pet) {
      await petStore.updatePet(props.pet.id, formData.value)
    } else {
      await petStore.createPet(formData.value)
    }
    
    emit('save')
    resetForm()
  } catch (err) {
    error.value = err.response?.data?.error || 'Wystąpił błąd'
  } finally {
    loading.value = false
  }
}

const close = () => {
  resetForm()
  emit('close')
}

const resetForm = () => {
  formData.value = {
    name: '',
    species: '',
    breed: '',
    age: null,
    weight: null,
    photo: null,
    tags: [],
    notes: ''
  }
  tagsInput.value = ''
  photoPreview.value = null
  error.value = null
}
</script>

<style scoped>
.modal.show {
  display: block;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: #000;
  opacity: 0.5;
}
</style>
