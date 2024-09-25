> 🫡 [catSirup](https://github.com/catSirup/KorEDA)님의 레포를 fork하여 수정한 것입니다.

# catSirup's KorEDA 

<details>
	<summary>catSirup님의 README.md</summary>
<p>
이 프로젝트는 <a href='https://github.com/jasonwei20/eda_nlp' target='_blank'>EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks</a> 를 한국어로 쓸 수 있도록 wordnet 부분만 교체한 프로젝트 입니다.
<br><br>
wordnet은 KAIST에서 만든 <a href='http://wordnet.kaist.ac.kr/' target='_blank'>Korean WordNet(KWN)</a> 을 사용했습니다.
<br><br>
EDA에 대한 자세한 내용은 <a href='https://arxiv.org/pdf/1901.11196.pdf' target='_blank'>논문</a>을 참조하시거나 <a href='https://catsirup.github.io/ai/2020/04/21/nlp_data_argumentation.html' target='_blank'>한글로 번역한 블로그</a>를 확인하시면 됩니다.
</p>

<h3>결과</h3>
<p>
원문 데이터
<pre><code class='plain'>
제가 우울감을 느낀지는 오래됐는데 점점 개선되고 있다고 느껴요
</code></pre>
data augmentation한 데이터
<pre><code class='plain'>
우울감을 느낀지는 오래됐는데 점점 개선되고 있다고	
제가 우울감을 느낀지는 오래됐는데 느껴요 개선되고 있다고 점점	
오래됐는데 우울감을 느낀지는 제가 점점 개선되고 있다고 느껴요	
느껴요 우울감을 느낀지는 오래됐는데 점점 개선되고 있다고 제가
</code></pre>
</p>

<h3>한계</h3>
<p>
WordNet만을 단순히 바꿔서 결괏값을 내기 때문에 의미가 변형되어버리는 경우가 생깁니다. 특히 SR과 RI를 사용할 때 많이 발생하는데 <b>제가 잘못한 건 아닌 것 같아요</b> 를 <b>제가 잘못한 총 아닌 것 같아요</b> (건 -> 총) 으로 바뀌기도 한다. 본 논문에서는 이렇게 바꿔도 꽤나 원문 데이터의 성질을 따라간다고 하지만.. 한국어의 특성상 완전히 따라가기에는 쉽지 않은 것 같다.
<br><br>
안전하게 데이터 증강을 하고 싶다면 RD, RS만을 사용하고, 데이터가 많이 필요하다싶으면 SR과 RI까지 사용하고 인간지능으로 데이터를 걸러내는 작업이 필요할 것이다.
</p>
</details>


# Update

오류가 발생하는 코드를 수정하고 편리한 함수를 정의하고 있습니다.
- 기존에는 한국어만 취급하고 있기 때문에 이를 수정 > `get_only_character` 추가

## Paragraph EDA

- `EDA_paragraph` : `EDA`는 한 문장만 입력받는다. 이 함수는 여러 여러 문장을 입력받아 그 중에서 랜덤하게 문장과 eda method를 선택해 증강한다.
    - 원문 데이터
    ```plain
    Google이 발표한 AutoAugment가 대표적인 선행 연구이다. 이는 강화학습을 통해 이미지 데이터셋에 가장 적합한 증강 정책을 자동으로 찾아주는 알고리즘이다. 대단히 많은 GPU 자원을 토대로 증강 방법을 최적화했을 때 다양한 task에서 우수한 성능을 보였다. 이 연구는 특히 대규모 데이터셋에서의 일반화 성능을 크게 향상시켰다. 이후 다양한 연구들이 이를 기반으로 데이터 증강을 더욱 효율적으로 수행하는 방법을 제안하고 있다.
    ```
    - `EDA_paragraph(test_paragraph, sentence_sep='.', alpha_sent=0.6, methods=['rs','rd'], method_alphas=[0.2,0.1], num_aug=2)` : test_paragraph의 5개 문장 중 3개(5 * 0.6)의 문장에 RS, RD method를 랜덤하게 적용하여 2개의 증강된 문단을 생성한다.
    - data augmentation 결과
    ```python
    ['Google이 발표한 AutoAugment가 대표적인 선행 연구이다. 이는 가장 통해 이미지 데이터셋에 강화학습을 찾아주는 증강 정책을 자동으로 적합한 알고리즘이다. 대단히 증강 GPU 자원을 토대로 성능을 방법을 최적화했을 때 다양한 task에서 우수한 많은 보였다. 일반화 연구는 특히 대규모 데이터셋에서의 이 성능을 크게 향상시켰다. 이후 다양한 연구들이 이를 기반으로 데이터 증강을 더욱 효율적으로 수행하는 방법을 제안하고 있다.', 
    'Google이 발표한 AutoAugment 가 대표적인 선행 연구이다. 통해 이미지 데이터셋에 증강 정책을 자동으로 찾아주는. 다양한 많은 GPU 자원을 토대로 증강 우수한 최적화했을 때 대단히 task에서 방법을 성능을 보였다. 이 연구는 특히 대규모 데이터셋에서의 일반화 성능을 크게 향상시켰다. 이후 다양한 연구들이 기반으로 데이터 증강을 더욱 효율적으로 수행하는 방법을 있다.']
    ```