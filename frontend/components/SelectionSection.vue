<script setup>
import { ref, computed } from 'vue'

const { getByKey, getAltByKey, getTitleByKey, getDescByKey } = await useSiteImages()

const grapes = [
    { 
        key: 'friendly_01',
        img: getByKey('friendly_01', '/images/friendly01.jpg'), 
        title: getTitleByKey('friendly_01', '友善大地'), 
        desc: getDescByKey('friendly_01', '這片溫暖肥沃的土地上，葡萄在自然與人之間找到最好的平衡。我們採用草生栽培方式，讓果園中的雜草自然生長，不僅保護土壤結構、減少水分流失，也為田間帶來更多有益生態，讓土地能夠自行呼吸與修復。') 
    },
    { 
        key: 'friendly_02',
        img: getByKey('friendly_02', '/images/friendly02.jpg'), 
        title: getTitleByKey('friendly_02', '陽光雨露'), 
        desc: getDescByKey('friendly_02', '彰化地區日照充足、雨水分布適中，為葡萄生長提供穩定而理想的環境。在枝條萌芽關鍵期，充足的陽光促進芽體活化，適量的水分則讓新梢生長均勻健壯，使葡萄能在良好的基礎下順利展開整個生長季。') 
    },
    { 
        key: 'friendly_03',
        img: getByKey('friendly_03', '/images/friendly03.png'), 
        title: getTitleByKey('friendly_03', '生態共鴨'), 
        desc: getDescByKey('friendly_03', '在葡萄園田間飼養鴨子，讓牠們成為天然的清道夫。鴨子能主動覓食田間害蟲與雜草，降低病蟲害發生，同時減少人為除蟲與化學用藥的需求。牠們的活動也促進土壤循環，形成自然共生的生態系統，讓葡萄在更健康的環境中成長。') 
    },
    { 
        key: 'friendly_04',
        img: getByKey('friendly_04', '/images/friendly04.png'), 
        title: getTitleByKey('friendly_04', '智慧溫室'), 
        desc: getDescByKey('friendly_04', '我們把最難照顧的環節，交給科技來完成。溫室設備結合機械化，減少病蟲害干擾，讓葡萄在穩定又乾淨的環境中慢慢長大，只留下更純粹、更美味的自然甜味。') 
    },
    { 
        key: 'friendly_05',
        img: getByKey('friendly_05', '/images/friendly05.jpg'), 
        title: getTitleByKey('friendly_05', '嚴選安心'), 
        desc: getDescByKey('friendly_05', '每一顆葡萄在出園前，皆經過嚴格篩檢與把關，以低農藥管理為基礎，檢測結果趨近於零農藥殘留。從田間到餐桌，清楚可追溯的來源，讓消費者安心品嚐每一口自然風味。') 
    }
]

// Default to index 0 (First Item)
const activeIndex = ref(0)

const currentGrape = computed(() => {
    return grapes[activeIndex.value]
})
</script>

<template>
    <section class="selection_section">
        <div class="selection_container">
            <!-- Single Side (Former Right Side) -->
            <div class="selection_col">
                <h3 class="selection_header">安心農產</h3>
                <div class="selection_display">
                    <div class="display_img_wrapper">
                        <!-- :key="activeIndex" forces re-render to restart animation -->
                        <img 
                            :src="currentGrape.img" 
                            :alt="currentGrape.title" 
                            class="display_img animate_float"
                            :key="activeIndex"
                        >
                    </div>
                    <div class="display_info_glass">
                        <div class="info_header">
                            <h2 class="display_title">{{ currentGrape.title }}</h2>
                        </div>
                        <p class="display_desc">
                            {{ currentGrape.desc }}
                        </p>
                    </div>
                </div>
                <div class="selection_choices_row">
                    <button 
                        v-for="(item, index) in grapes" 
                        :key="index"
                        class="choice_btn" 
                        :class="{ active: activeIndex === index }"
                        @click="activeIndex = index"
                    >
                        <img :src="item.img" :alt="item.title">
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>


<style src="@/assets/css/SelectionSection.css" scoped></style>
