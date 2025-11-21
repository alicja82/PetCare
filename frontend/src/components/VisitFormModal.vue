<template>
  <div class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ visit ? 'Edytuj wizytę' : 'Dodaj wizytę weterynaryjną' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <!-- Pet selection -->
            <div class="mb-3" v-if="!visit && pets.length > 0">
              <label class="form-label">Zwierzę *</label>
              <select class="form-select" v-model="form.pet_id" required>
                <option value="">Wybierz zwierzę...</option>
                <option v-for="pet in pets" :key="pet.id" :value="pet.id">
                  {{ pet.name }}
                </option>
              </select>
            </div>

            <div class="row">
              <!-- Visit date -->
              <div class="col-md-6 mb-3">
                <label class="form-label">Data wizyty *</label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="form.visit_date"
                  required
                />
              </div>

              <!-- Cost -->
              <div class="col-md-6 mb-3">
                <label class="form-label">Koszt (zł)</label>
                <input 
                  type="number" 
                  step="0.01"
                  class="form-control" 
                  v-model="form.cost"
                  placeholder="np. 150.00"
                />
              </div>
            </div>

            <!-- Reason -->
            <div class="mb-3">
              <label class="form-label">Powód wizyty *</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.reason"
                placeholder="np. Szczepienie, Kontrola, Choroba"
                required
              />
            </div>

            <!-- Vet name -->
            <div class="mb-3">
              <label class="form-label">Weterynarz</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="form.vet_name"
                placeholder="Imię i nazwisko weterynarza"
              />
            </div>

            <!-- Diagnosis -->
            <div class="mb-3">
              <label class="form-label">Diagnoza</label>
              <textarea 
                class="form-control" 
                v-model="form.diagnosis"
                rows="2"
                placeholder="Opis diagnozy..."
              ></textarea>
            </div>

            <!-- Treatment -->
            <div class="mb-3">
              <label class="form-label">Leczenie</label>
              <textarea 
                class="form-control" 
                v-model="form.treatment"
                rows="2"
                placeholder="Zalecone leczenie, leki, zalecenia..."
              ></textarea>
            </div>

            <!-- Notes -->
            <div class="mb-3">
              <label class="form-label">Notatki</label>
              <textarea 
                class="form-control" 
                v-model="form.notes"
                rows="3"
                placeholder="Dodatkowe informacje..."
              ></textarea>
            </div>

            <div class="text-end">
              <button type="button" class="btn btn-secondary me-2" @click="$emit('close')">
                Anuluj
              </button>
              <button type="submit" class="btn btn-success" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ visit ? 'Zapisz' : 'Dodaj' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useVisitStore } from '../stores/visit'

const props = defineProps({
  visit: Object,
  pets: Array,
  selectedPetId: Number
})

const emit = defineEmits(['close', 'save'])

const visitStore = useVisitStore()
const loading = ref(false)

const form = ref({
  pet_id: props.selectedPetId || (props.visit?.pet_id || ''),
  visit_date: props.visit?.visit_date || new Date().toISOString().split('T')[0],
  reason: props.visit?.reason || '',
  diagnosis: props.visit?.diagnosis || '',
  treatment: props.visit?.treatment || '',
  vet_name: props.visit?.vet_name || '',
  cost: props.visit?.cost || '',
  notes: props.visit?.notes || ''
})

watch(() => props.selectedPetId, (newVal) => {
  if (newVal && !props.visit) {
    form.value.pet_id = newVal
  }
})

const handleSubmit = async () => {
  loading.value = true
  try {
    // Convert cost to number or null
    const submitData = {
      ...form.value,
      cost: form.value.cost ? parseFloat(form.value.cost) : null
    }

    if (props.visit) {
      // Update existing visit
      await visitStore.updateVisit(props.visit.id, submitData)
    } else {
      // Create new visit
      await visitStore.createVisit(submitData.pet_id, submitData)
    }
    emit('save')
  } catch (error) {
    // Error is handled in store
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal.show {
  display: block;
}
</style>
