<script setup>
import { reactive } from 'vue'

const faqCategories = reactive([
    {
        title: '關於葡萄',
        className: 'faq_block',
        bubbleText: '關於葡萄',
        list: [
            {
                question: '什麼時候的葡萄最好吃？',
                answer: '我們的葡萄產季通常從 6 月開始至 12 月（依品種而定）。夏季的巨峰葡萄香氣最濃郁，冬季的溫室葡萄則口感更為細緻香甜。',
                isOpen: true
            },
            {
                question: '葡萄表皮的白色粉末是什麼？',
                answer: '那是天然的「果粉」，是葡萄健康、新鮮的證明！果粉能保護果實防止水分蒸發，食用時只需輕輕沖洗即可。',
                isOpen: true
            },
            {
                question: '我可以選擇葡萄的甜度嗎？',
                answer: '田原葡萄堅持完熟採收，甜度保證在 18 度以上。雖然無法針對單串指定甜度，但我們的品質控管嚴格，保證每一串都香甜可口。',
                isOpen: true
            }
        ]
    },
    {
        title: '如何訂購和運送',
        className: 'faq_block shipping',
        bubbleText: '如何訂購<br>和運送',
        list: [
            {
                question: '下單後多久會收到？',
                answer: '確認訂單並完成付款後，我們將於 1-3 個工作天內採摘並安排出貨（黑貓冷藏宅配），確保您收到最新鮮的葡萄。',
                isOpen: true
            },
            {
                question: '運費如何計算？',
                answer: '單筆消費滿 NT$2,000 即享免運費優惠。未滿額則酌收 NT$160 冷藏運費。',
                isOpen: true
            },
            {
                question: '收到商品有問題怎麼辦？',
                answer: '若收到商品時發現有嚴重損傷或品質問題，請於收到當日拍照並聯繫我們的客服，我們將盡速為您處理。',
                isOpen: true
            }
        ]
    }
])

</script>

<template>
    <section class="faq_section">
        <div class="faq_container">
            <!-- Header -->
            <div class="faq_page_title">
                <h2>Q&A</h2>
                <span>常見問題</span>
            </div>

            <div 
                v-for="(category, catIndex) in faqCategories" 
                :key="catIndex"
                :class="category.className"
            >
                <div class="faq_category">
                    <div class="faq_category_bubble" v-html="category.bubbleText"></div>
                </div>
                <div class="faq_list">
                    <div 
                        v-for="(item, itemIndex) in category.list" 
                        :key="itemIndex"
                        class="faq_item"
                        :class="{ active: item.isOpen }"
                    >
                        <button class="faq_question" style="cursor: default;">
                            {{ item.question }}
                        </button>
                        <div class="faq_answer">
                            <p>{{ item.answer }}</p>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </section>
</template>

<style src="@/assets/css/FaqSection.css" scoped></style>